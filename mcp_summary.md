# Model Context Protocol (MCP) - Architecture Overview

## Introduction

The Model Context Protocol (MCP) is a protocol for context exchange between AI applications and external services. MCP focuses solely on the protocol for context exchange—it does not dictate how AI applications use LLMs or manage the provided context.

## Scope

The Model Context Protocol includes the following projects:

* **MCP Specification**: A specification of MCP that outlines the implementation requirements for clients and servers.
* **MCP SDKs**: SDKs for different programming languages that implement MCP.
* **MCP Development Tools**: Tools for developing MCP servers and clients, including the MCP Inspector
* **MCP Reference Server Implementations**: Reference implementations of MCP servers.

## Core Concepts

### Participants

MCP follows a client-server architecture with three key participants:

* **MCP Host**: The AI application (like Claude Code or Claude Desktop) that coordinates and manages one or multiple MCP clients
* **MCP Client**: A component that maintains a connection to an MCP server and obtains context from an MCP server for the MCP host to use
* **MCP Server**: A program that provides context to MCP clients

**Architecture Pattern**: Each MCP client maintains a dedicated one-to-one connection with its corresponding MCP server.

### Layers

MCP consists of two layers:

#### 1. Data Layer (Inner Layer)
The data layer implements a JSON-RPC 2.0 based exchange protocol that defines:

* **Lifecycle management**: Handles connection initialization, capability negotiation, and connection termination
* **Server features**: Enables servers to provide core functionality including:
  - Tools for AI actions
  - Resources for context data
  - Prompts for interaction templates
* **Client features**: Enables servers to:
  - Sample from the host LLM
  - Elicit input from the user
  - Log messages to the client
* **Utility features**: Supports notifications and progress tracking

#### 2. Transport Layer (Outer Layer)
The transport layer manages communication channels and authentication:

* **Stdio transport**: Uses standard input/output streams for direct process communication between local processes
* **Streamable HTTP transport**: Uses HTTP POST for client-to-server messages with optional Server-Sent Events

## Data Layer Protocol

### Lifecycle Management
MCP requires lifecycle management to negotiate capabilities that both client and server support through an initialization sequence.

### Primitives

MCP primitives are the most important concept within MCP. They define what clients and servers can offer each other.

#### Server Primitives
* **Tools**: Executable functions that AI applications can invoke to perform actions (e.g., file operations, API calls, database queries)
* **Resources**: Data sources that provide contextual information to AI applications (e.g., file contents, database records, API responses)
* **Prompts**: Reusable templates that help structure interactions with language models (e.g., system prompts, few-shot examples)

Each primitive type has associated methods for discovery (`*/list`), retrieval (`*/get`), and in some cases, execution (`tools/call`).

#### Client Primitives
* **Sampling**: Allows servers to request language model completions from the client's AI application using the `sampling/complete` method
* **Elicitation**: Allows servers to request additional information from users using the `elicitation/request` method
* **Logging**: Enables servers to send log messages to clients for debugging and monitoring

#### Utility Primitives
* **Tasks (Experimental)**: Durable execution wrappers that enable deferred result retrieval and status tracking for MCP requests

### Notifications
The protocol supports real-time notifications to enable dynamic updates between servers and clients. Notifications are sent as JSON-RPC 2.0 notification messages without expecting a response.

## Example Workflow

### 1. Initialization (Lifecycle Management)
The client sends an initialize request to establish connection and negotiate supported features:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

**Key aspects of initialization:**
- Protocol Version Negotiation ensures compatibility
- Capability Discovery allows each party to declare supported features
- Identity Exchange provides identification and versioning information

### 2. Tool Discovery
The client discovers available tools using `tools/list`:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

The response provides comprehensive metadata about each tool including name, title, description, and inputSchema.

### 3. Tool Execution
The client executes a tool using `tools/call`:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "weather_current",
    "arguments": {
      "location": "San Francisco",
      "units": "imperial"
    }
  }
}
```

**Key elements:**
- Name must match exactly the tool name from discovery
- Arguments contain input parameters as defined by the tool's inputSchema
- Response returns an array of content objects with flexible content types

### 4. Real-time Updates (Notifications)
Servers can send notifications about changes:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

**Benefits of notifications:**
- Dynamic environments can adapt to changing tools
- Efficient - no need for polling
- Ensures clients have accurate information
- Enables real-time collaboration

## How This Works in AI Applications

1. **Initialization**: AI application's MCP client manager establishes connections to configured servers and stores their capabilities
2. **Tool Discovery**: Application fetches available tools from all connected MCP servers and combines them into a unified tool registry for the language model
3. **Tool Execution**: When the LLM decides to use a tool, the application intercepts the call, routes it to the appropriate MCP server, executes it, and returns results
4. **Real-time Updates**: When notifications are received, the application refreshes its tool registry and updates the LLM's available capabilities

The Model Context Protocol enables AI applications to access real-time data and perform actions in the external world through a standardized, extensible interface.