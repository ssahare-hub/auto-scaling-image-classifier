var socket;
const WAIT_CONNECT_MSG = 'Establishing connection with server...'
const START_PROCESS_MSG = 'All images uploaded successfully, Image Processing was started in parallel';
function connect() {
    var url = 'http://' + document.domain + ':' + location.port
    console.log('url', url)
    socket = io.connect(url);
    console.log('socket id ', socket['id']);

    socket.on('connect', function () {
        console.log('connected socket-io');
        const SERVER_ESTB_MSG = 'Connection with server established...';
        displayMessage(SERVER_ESTB_MSG);

        // on upload start, change message
        socket.on('upload_start', (data) => {
            const START_UPLOAD_MSG = `Uploading of ${data} valid images started, waiting on processing...`;
            displayMessage(START_UPLOAD_MSG);
        });

        // on processing start, change message
        socket.on('processing_start', () => {
            displayMessage(START_PROCESS_MSG);
        });

        // on processing end, change message
        socket.on('processing_end', (data) => {
            const END_PROCESS_MSG = 'Processing Complete, results are displayed below -> ';
            displayMessage(END_PROCESS_MSG);
        })
        // on disconnect show connect option ->
        socket.on('disconnect', () => {
            const DISC_MSG = 'Connection to server has been lost, retrying connection...';
            displayMessage(DISC_MSG);
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
