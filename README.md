# T-Reqs HTTP Fuzzer

T-Reqs (**T**wo **Req**uest**s**) is a grammar-based HTTP Fuzzer written as a part of the paper titled "T-Reqs: HTTP Request Smuggling with Differential Fuzzing".

## About

T-Reqs is for fuzzing HTTP servers by sending confusing HTTP requests with versions 1.1 and earlier. It has three main components: 1) generating inputs, 2) mutating generated inputs and 3) delivering them to the target server(s). 

### Generating Inputs

A CFG grammar fed into the fuzzer is used to generate HTTP requests. As the example grammar shown below is tailored for request line fuzzing, every request line component and possible values for each of them are explicitly specified. This allows us to generate valid requests with various forms of request line and also to treat each request line component as a separate unit from the mutation perspective.

```     	
 '<start>':
     ['<request>'],
 '<request>':
     ['<request-line><base><the-rest>'],
 '<request-line>':
     ['<method-name><space><uri><space><protocol><separator><version><newline>'],
 '<method-name>':
     ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'],
 '<space>':
     [' '],
 '<uri>':
     ['/_URI_'],
 '<protocol>':
     ['HTTP'],
 '<separator>':
     ['/'],
 '<version>':
     ['0.9', '1.0', '1.1'],
 '<newline>':
     ['\r\n'],
 '<base>':
     ['Host: _HOST_\r\nConnection:close\r\nX-Request-ID: _REQUEST_ID_\r\n'],
 '<the-rest>':
     ['Content-Length: 5\r\n\r\nBBBBBBBBBB'],
```
### Mutating Inputs
Each component can be marked in two ways: string mutable and tree mutable ([see the example config](../main/config)). If a component is string mutable, then a random character can be deleted, replaced, or inserted at a random position. In the example shown below (left side), the last character in the protocol version (*1*) is deleted, the third letter in the method name (*S*) is replaced with *R*, and a forward slash is inserted at the beginning of the URI. Whereas, if a component is tree mutable, then a random component can be deleted, replaced, or inserted at a random position under that component. The example below (right side) shows three tree mutations applied on the request line component: 1) *method* is replaced by *protocol*, 2) an extra *URI* is inserted after the current URI, and 3) the existing *proto* is deleted. 

![Mutation Types](figs/mutation-types.png) 

## Usage

## Using for Finding HRS discrepancies
