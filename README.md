# T-Reqs HTTP Fuzzer

T-Reqs is a grammar-based HTTP Fuzzer written as a part of the paper titled "T-Reqs: HTTP Request Smuggling with Differential Fuzzing".

## About

<!--T-Reqs can generate, mutate and deliver HTTP requests with the version 1.1 and earlier. To generate inputs, the fuzzer uses a user-specified CFG grammar, which lets users to describe the structure of HTTP requests. Generated inputs can be mutated by two types of mutations: string and tree. Users specify which type of mutations will be applied to which part of a request. Maximum and minimum number of mutations to be a applied on a request can also be decided by users. All of these user choices are fed into the fuzzer in a configuration file, for which an [example](../main/config) is available in this repo.-->
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
Each component can be marked in two ways: string-mutable and tree-mutable ([see the example config](../main/config)). If a component is string-mutable, then random characters can be inserted, replaced or removed at a random positions. 

## Usage

## Using for Finding HRS discrepancies
