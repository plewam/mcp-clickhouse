from .mcp_server import mcp
from .mcp_env import get_mcp_config, get_config, get_chdb_config, TransportType
import logging

logger = logging.getLogger("mcp-clickhouse")


def log_configuration():
    """Log all configuration values on startup."""
    logger.info("Starting MCP ClickHouse Server")

    # MCP Server Config
    mcp_config = get_mcp_config()
    logger.info("MCP Server Configuration:")
    logger.info(f"  Transport: {mcp_config.server_transport}")
    logger.info(f"  Bind Host: {mcp_config.bind_host}")
    logger.info(f"  Bind Port: {mcp_config.bind_port}")
    logger.info(f"  Query Timeout: {mcp_config.query_timeout}")

    # ClickHouse Config
    ch_config = get_config()
    logger.info("ClickHouse Configuration:")
    logger.info(f"  Enabled: {ch_config.enabled}")
    if ch_config.enabled:
        logger.info(f"  Host: {ch_config.host}")
        logger.info(f"  Port: {ch_config.port}")
        logger.info(f"  User: {ch_config.username}")
        # Mask password
        masked_password = "*" * 8 if ch_config.password else "None"
        logger.info(f"  Password: {masked_password}")
        logger.info(f"  Database: {ch_config.database}")
        logger.info(f"  Secure: {ch_config.secure}")
        logger.info(f"  Verify SSL: {ch_config.verify}")
        logger.info(f"  Role: {ch_config.role}")
        logger.info(f"  Proxy Path: {ch_config.proxy_path}")

    # chDB Config
    chdb_config = get_chdb_config()
    logger.info("chDB Configuration:")
    logger.info(f"  Enabled: {chdb_config.enabled}")
    if chdb_config.enabled:
        logger.info(f"  Data Path: {chdb_config.data_path}")


def main():
    log_configuration()
    mcp_config = get_mcp_config()
    transport = mcp_config.server_transport

    # For HTTP and SSE transports, we need to specify host and port
    http_transports = [TransportType.HTTP.value, TransportType.SSE.value]
    if transport in http_transports:
        # Use the configured bind host (defaults to 127.0.0.1, can be set to 0.0.0.0)
        # and bind port (defaults to 8000)
        mcp.run(transport=transport, host=mcp_config.bind_host, port=mcp_config.bind_port)
    else:
        # For stdio transport, no host or port is needed
        mcp.run(transport=transport)


if __name__ == "__main__":
    main()
