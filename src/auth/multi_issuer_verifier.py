"""Multi-issuer JWT verifier for supporting both OAuth and session tokens."""

from __future__ import annotations

import time
from typing import Any

from authlib.jose.errors import JoseError

from fastmcp.server.auth import AccessToken
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)


class MultiIssuerJWTVerifier(JWTVerifier):
    """
    JWT verifier that accepts tokens from multiple issuers.

    This extends JWTVerifier to support validating tokens that may come from:
    - OAuth2 DCR flow: issuer = https://api.descope.com/v1/apps/{project_id}
    - Session tokens: issuer = {project_id} (just the project ID, per Descope docs)

    Both token types use the same JWKS endpoint for signature validation.

    Usage:
        verifier = MultiIssuerJWTVerifier(
            issuers=[
                f"https://api.descope.com/v1/apps/{project_id}",  # OAuth tokens
                project_id,  # Session tokens
            ],
            jwks_uri=f"https://api.descope.com/{project_id}/.well-known/jwks.json",
            audience=project_id,
        )
    """

    def __init__(
        self,
        *,
        issuers: list[str],
        jwks_uri: str,
        audience: str | list[str] | None = None,
        algorithm: str = "RS256",
        required_scopes: list[str] | None = None,
    ):
        """
        Initialize with multiple allowed issuers.

        Args:
            issuers: List of valid issuer values (any one must match)
            jwks_uri: URI to fetch JSON Web Key Set
            audience: Expected audience claim(s)
            algorithm: JWT signing algorithm (default RS256)
            required_scopes: Required scopes for all tokens
        """
        if not issuers:
            raise ValueError("At least one issuer must be provided")

        # Initialize parent with first issuer (parent requires issuer for logging)
        # We'll override the issuer validation in load_access_token
        super().__init__(
            jwks_uri=jwks_uri,
            issuer=issuers[0],  # Parent stores this, but we override validation
            audience=audience,
            algorithm=algorithm,
            required_scopes=required_scopes,
        )

        # Store all valid issuers for our custom validation
        self.valid_issuers = set(issuers)

    async def load_access_token(self, token: str) -> AccessToken | None:
        """
        Validate JWT token, accepting any of the configured issuers.

        This overrides the parent's load_access_token to support multi-issuer
        validation instead of strict single-issuer matching.

        Args:
            token: The JWT token string to validate

        Returns:
            AccessToken object if valid, None if invalid or expired
        """
        try:
            # Get verification key (from JWKS)
            verification_key = await self._get_verification_key(token)

            # Decode and verify the JWT token signature
            claims = self.jwt.decode(token, verification_key)

            # Extract client ID early for logging
            client_id = claims.get("client_id") or claims.get("sub") or "unknown"

            # Validate expiration
            exp = claims.get("exp")
            if exp and exp < time.time():
                logger.debug(
                    "Token validation failed: expired token for client %s", client_id
                )
                return None

            # Multi-issuer validation (our custom logic)
            token_issuer = claims.get("iss")
            if token_issuer not in self.valid_issuers:
                logger.debug(
                    "Token validation failed: issuer mismatch for client %s. "
                    "Token issuer: %s, Valid issuers: %s",
                    client_id,
                    token_issuer,
                    self.valid_issuers,
                )
                return None

            # Validate audience if configured AND token has an audience claim
            # Note: Descope session tokens may not include 'aud' claim, so we skip
            # audience validation for tokens without it. OAuth tokens typically include it.
            aud = claims.get("aud")
            if self.audience and aud is not None:
                audience_valid = False

                if isinstance(self.audience, list):
                    if isinstance(aud, list):
                        audience_valid = any(
                            expected in aud for expected in self.audience
                        )
                    else:
                        audience_valid = aud in self.audience
                else:
                    if isinstance(aud, list):
                        audience_valid = self.audience in aud
                    else:
                        audience_valid = aud == self.audience

                if not audience_valid:
                    logger.debug(
                        "Token validation failed: audience mismatch for client %s. "
                        "Token audience: %s, Expected: %s",
                        client_id,
                        aud,
                        self.audience,
                    )
                    return None

            # Extract scopes using parent's helper method
            scopes = self._extract_scopes(claims)

            # Check required scopes if configured
            if self.required_scopes:
                token_scopes = set(scopes)
                required_scopes = set(self.required_scopes)
                if not required_scopes.issubset(token_scopes):
                    logger.debug(
                        "Token missing required scopes. Has: %s, Required: %s",
                        token_scopes,
                        required_scopes,
                    )
                    return None

            return AccessToken(
                token=token,
                client_id=str(client_id),
                scopes=scopes,
                expires_at=int(exp) if exp else None,
                claims=claims,
            )

        except JoseError:
            logger.debug("Token validation failed: JWT signature/format invalid")
            return None
        except Exception as e:
            logger.debug("Token validation failed: %s", str(e))
            return None

    async def verify_token(self, token: str) -> AccessToken | None:
        """
        Verify a bearer token and return access info if valid.

        Implements the TokenVerifier protocol by delegating to load_access_token.

        Args:
            token: The JWT token string to validate

        Returns:
            AccessToken object if valid, None if invalid or expired
        """
        return await self.load_access_token(token)
