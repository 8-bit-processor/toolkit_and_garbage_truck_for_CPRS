import http from 'http';
import { Ollama } from 'ollama';
const ollama = new Ollama;

// Function to fetch ollama response with Async/Await
async function ollamaResponse(userInput) {
    const response = await ollama.chat({
        model: 'tinyllama',
        messages: [{ role: 'user', content:userInput }],
    });
    var outputMessage = response.message.content;
    console.log(outputMessage);
    return outputMessage;
};


//create server that takes request object and sends response object
var server = http.createServer(function(req,res){
    // what page is being requested- show the page the user was trying to access
    console.log('request was made: ' + req.url);
    let body = '';
    req.on('data', (chunk) => {
        body += chunk;
    });
    req.on('end', () => {
        try {
            let postObject = JSON.stringify(body);
            console.log('Received POST request with data: ', postObject);
            let postData = JSON.parse(postObject)
            // response header  tells browser about content-type and
            // status code- whether transmission was ok or failed
            res.setHeader( "access-control-allow-origin",'*');
            // repsond with a message in the header
            // response header  tells browser about content-type and 
            // status code- whether transmission was ok or failed  
            res.writeHead(200, {'content-type': 'text/plain',
                "access-control-allow-origin":"*"});
            // repsond with a message in the header
            console.log("sending data to ollama:", postData)
            ollamaResponse(postData).then((outputMessage) => {
            res.end(outputMessage);
            });
        } catch (error) {
            console.error('Error processing POST request:', error);
        };
    });
});

// start server listening on port 3000 <--server will respond thru this port
// at local ip address 127.0.0.1 <-- replace with TMTlabs ip address later


server.listen(3000,'127.0.0.1');
console.log('Hello world TMTlabs.com server hosting at 127.0.0.1 and listening to port 3000');