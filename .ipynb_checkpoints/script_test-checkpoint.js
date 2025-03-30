// script.js

function readHL7File() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
      alert('Please select a file');
      return;
    }
  
    const reader = new FileReader();
    
    reader.onload = function(e) {
      const hl7Message = e.target.result;
      const parsedMessage = parseHL7Message(hl7Message);
      displayHL7Content(parsedMessage);
    };
  
    reader.onerror = function() {
      alert('Error reading file');
    };
  
    reader.readAsText(file);
  }
  
  function parseHL7Message(hl7Message) {
    // HL7 messages are typically pipe-separated and sometimes carets (^), tilde (~), or ampersand (&) are used as delimiters.
    
    const segments = hl7Message.split('\n'); // Split by line (each segment is on a new line)
    let parsedMessage = '<ul>';
  
    segments.forEach((segment) => {
      const fields = segment.split('|'); // Split each segment by pipe (|) character
      parsedMessage += '<li><strong>' + fields[0] + ':</strong><ul>'; // Show the segment type (e.g., MSH, PID)
      
      fields.slice(1).forEach((field, index) => {
        parsedMessage += `<li>Field ${index + 1}: ${field}</li>`; // Display each field in the segment
      });
      
      parsedMessage += '</ul></li>';
    });
  
    parsedMessage += '</ul>';
    return parsedMessage;
  }
  
  function displayHL7Content(parsedMessage) {
    const hl7ContentDiv = document.getElementById('hl7Content');
    hl7ContentDiv.innerHTML = parsedMessage;
  }
  