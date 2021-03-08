var socket;
const WAIT_CONNECT_MSG = 'Establishing connection with server...'
const START_PROCESS_MSG = 'All images uploaded successfully, Image Processing was started in parallel';
const CONTINUE_PROCESS_MSG = 'Info about results processed is -> ';
function connect() {
    var url = 'http://' + document.domain + ':' + location.port
    console.log('url', url)
    socket = io.connect(url);
    console.log('socket id ', socket['id']);
    var counter = 0;
    var total = 0;
    socket.on('connect', function () {
        console.log('connected socket-io');
        const SERVER_ESTB_MSG = 'Connection with server established...';
        displayMessage(SERVER_ESTB_MSG);
        
        // on upload start, change message
        socket.on('upload_start', (data) => {
            console.log('upload_Start')
            const START_UPLOAD_MSG = `Uploading of ${data} valid images started, waiting on processing...`;
            displayMessage(START_UPLOAD_MSG);
        });
        
        // on processing start, change message
        socket.on('processing_start', (all) => {
            console.log('processing_start')
            counter = 0;
            total = all;
            displayMessage(START_PROCESS_MSG);
        });
        
        // on processing end, change message
        socket.on('processing_end', () => {
            console.log('processing_end')
            const END_PROCESS_MSG = 'Processing Complete, all results have loaded below -> ';
            displayMessage(END_PROCESS_MSG);
        })
        // on disconnect show connect option ->
        socket.on('disconnect', () => {
            console.log('disconnected')
            const DISC_MSG = 'Connection to server has been lost, retrying connection...';
            displayMessage(DISC_MSG);
        })
        socket.on('partial_result', (result) => {
            console.log('part_result',result)
            counter+=1;
            addResults(result);
            displayMessage(CONTINUE_PROCESS_MSG+`${counter} / ${total}`);
        })
    });
}

connect()

function displayMessage(message) {
    var x = document.getElementById('info');
    if (x) {
        x.innerText = message;
    }
}

function addResults(result)
{
    var x = document.getElementById('results')
    if(x){
        var y = document.createElement('p')
        y.innerText = result
        x.appendChild(y)
    }
}