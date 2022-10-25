
    'use strict'

    var constraints = {
            audio : true,
    };
    var recorder = null;
    var audioStream = null;
    var audioData = null;
    var audioContext = null;
    var csrftoken = getCookie('csrftoken');
    var socket = null;
    var interval;
    
    var stt_id = '';
    var params = (new URL(window.location)).searchParams;
    stt_id = params.get("stt_id");
    
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }


    function protocolHandler(){
    	if($('#ws-radio').prop('checked')){
    		$('#file').prop('disabled', true);
    		$('#submitAudio').prop('disabled', true);
    	} else {
    		$('#file').prop('disabled', false);
    		$('#submitAudio').prop('disabled', false);
    	}
    }


    function initWebSocket(){
    	if(!socket){
    		socket = new WebSocket('ws://127.0.0.1:8000/dsserver/');

    		socket.onopen = function(){
    			interval = setInterval(function(){
    				recorder.exportWAV(function(blob){
    		            audioData = blob;
    		            if(socket && socket.readyState == WebSocket.OPEN){
    		            	socket.send(audioData);
    		            }
    		        }, false);
    			}, 2000);
    		}

    		socket.onmessage = function(res){
    			$('#transcription-result').text(res.data);
    		}

    		socket.onerror = function(error){
    			alert('web socket error: ' + error);
    		}

    		socket.onclose = function(e){
    			clearInterval(interval);
    			console.log('websocket closed');
    		}

    	}
    }


    function closeWebSocket(){
    	if(socket && socket.readyState != WebSocket.CLOSED){
    		socket.close();
    	}
		socket = null;
    }


    function startRecording(){
    	$("#file").val("");
    	if (navigator.mediaDevices.getUserMedia === undefined) {
    		displayError("This browser doesn't support getUserMedia.");
    	}
        navigator.mediaDevices.getUserMedia(constraints)
        .then(function(stream){
        	audioStream = stream;
            if(!audioContext){
                audioContext = new AudioContext();
            }
            var source = audioContext.createMediaStreamSource(stream);
            recorder = audioRecorder.fromSource(source);
            recorder.record();
            if($('#ws-radio').prop('checked') && !socket){
            	initWebSocket();
            } else if(socket){
            	closeWebSocket();
            }
        })
        .catch(function(err){
        	displayError("Error occurred while getting audio stream: " + err);
        })
    }


    function stopRecording(){
    	recorder.stop();
    	clearInterval(interval);
        recorder.exportWAV(function(blob){
            audioStream.getTracks()[0].stop();
            audioStream = null;
            audioData = blob;
            var url = URL.createObjectURL(blob);
            var mt = document.createElement('audio');
            mt.controls = true;
            mt.src = url;
            $('#player')[0].innerHTML = "";
            $('#player').append(mt);
            if(socket && socket.readyState == WebSocket.OPEN){
            	socket.send(audioData);
            	closeWebSocket();
            }
        }, true);
        recorder.clear();
    }


    function submitToServer(){
        
        if(audioData == null) {
            displayError("There is no audio data here!");
            return;
        }

        $('#error-panel').hide();
        $('#progress-panel').show();
        $('#btnSRT').hide();
        $('#btnJson').hide(); 
		$('#btnCSV').hide();
        $('#btnStatus').hide();
        $("#btnEditTranscription").hide();
        
        $('.progress-bar').css('width', '0%').attr('aria-valuenow', 0);
        
        var formData = new FormData();
        formData.append("soundfile", audioData);
        $.ajax({
          xhr: function() {
            var xhr = new  XMLHttpRequest();
            xhr.upload.addEventListener('progress', function(e){
                if (e.lengthComputable) {
                var uploadPercent = e.loaded / e.total;
                    uploadPercent = (uploadPercent * 100);
                    console.log(uploadPercent);
                    $('.progress-bar').width(uploadPercent + '%');
                } else {
                    console.log('not computable');
                }
            }, false); 
            return xhr;
          },
          url: "../speech_to_text/",
          type: "POST",
          contentType: false,
          processData: false,
          data: formData,
          headers: {
            'X-CSRFTOKEN': csrftoken
          },
          success: function(response){
            stt_id = response.id;
            $('#transcriptions-panel').show();
            $('#btnStatus').show();          
            $('#progress-panel').hide();
            $('#transcription-id').text(stt_id);  
          },
          error: function(response){
            $('#transcription-id').text(response.responseText);
            $('#progress-panel').hide();
          }
        });
    }


    function submitGetStatus(){
      $('#status-panel').show();
      $.ajax({
		url: "../get_status",
        type: "GET",
        data: {
	    "stt_id": stt_id
	},
	success: function(response){
        var status = response.status;
        var currenttext = $('#status').text();
        if (status == "SUCCESS"){                        
            $('#btnSRT').show();
            $('#btnJson').show(); 
			$('#btnCSV').show();  
            $("#btnEditTranscription").show();
                
                //
                $.ajax({
                        url: "../get_json",
                        type: "GET",
                        data: {
                            "stt_id": stt_id
			        },
			        success: function(response){
			            var str = JSON.stringify(response, null, 2); // spacing level = 2
			            $('#transcription-result').text(str);
			        },
			        error: function(response){
			            $('#transcription-result').text(response.responseText);
			        }
		        });                
	        }
	        $('#status').text(currenttext + "\n" + response.status);
	    },
	error: function(response){
            $('#status-message').text(response.responseText);
            $('#progress-panel').hide();
	}
      });
    }

    function editTranscriptions(){
    	//
    	$.ajax({
		url: "../get_json",
		type: "GET",
		data: {
		    "stt_id": stt_id
		},
		success: function(response){
		    //
		    $('#transcription-result').empty();
		
		    //
		    var base_audio_url =  window.location.protocol + "//" + window.location.host + window.location.pathname;
                    base_audio_url = base_audio_url.replace("index.html", "../get_audio?stt_id=" + stt_id);
                    
                    //
		    var table = $('<table/>'), table_head = $('<thead/>'), head_row = $('<tr/>'), table_body = $('<tbody/>'), body_row = [];
		    
		    head_row.append("<th>Index</th>");
		    head_row.append("<th/>");
		    head_row.append("<th>Start</th>");
		    head_row.append("<th>End</th>");
		    head_row.append("<th>Transcript</th>");
		    
		    table_head.append(head_row);
		    table.append(table_head);
	
		    //
		    $.each(response, function(i, trans_obj) {
		    	//
		    	if (trans_obj.text.length > 0) {
      				body_row[i] = $('<tr/>');
      				body_row[i].append('<td>' + i + '</td>');
      				
      				var audio_url = base_audio_url + "&start=" + trans_obj.start + "&end=" + trans_obj.end;
      				var audio = $("<audio/>").attr({'src':audio_url, 'controls':true});
      				var audio_td = $("<td/>");
      				
      				audio_td.append(audio);
      				body_row[i].append(audio_td);
    				
    				body_row[i].append('<td>' + trans_obj.start + '</td>');
    				body_row[i].append('<td>' + trans_obj.end + '</td>');
    				body_row[i].append('<td>' + trans_obj.text + '</td>');
    			} else {
    				body_row[i] = $('<tr/>');
      				body_row[i].append('<td>' + i + '</td>');
    				body_row[i].append('<td/>');
    				body_row[i].append('<td/>');
    				body_row[i].append('<td/>');
    				body_row[i].append('<td/>');
    			}
		    });
		    
		    //
		    table_body.append(body_row);
		    table.append(table_body);
		    
		    table.addClass('table').addClass('table-bordered');

		    $('#transcription-result').html(table);
		    
		},
		error: function(response){
		    $('#transcription-result').text(response.responseText);
		}
	});
    }
    
    
    function submitGetSrt(){
    	var srt_url =  window.location.protocol + "//" + window.location.host + window.location.pathname;
        srt_url = srt_url.replace("index.html", "../get_srt?stt_id=" + stt_id);
        window.open(srt_url, "", "_blank");
	}


	function submitGetCsv(){
		var srt_url =  window.location.protocol + "//" + window.location.host + window.location.pathname;
		srt_url = srt_url.replace("index.html", "../get_csv?stt_id=" + stt_id);
		window.open(srt_url, "", "_blank");
    }

	
    function submitGetJson(){
    	var json_url =  window.location.protocol + "//" + window.location.host + window.location.pathname;
        json_url = json_url.replace("index.html", "../get_json?stt_id=" + stt_id);
        window.open(json_url, "", "_blank");
    }
    

    var openFile = function(event) {
        var input = event.target;
        var isValid = checkValidity(input.files[0]);
        if(!isValid){
        	displayError("Only wav file type allowed.");
        	return;
        }
        var url = URL.createObjectURL(input.files[0]);
        var mt = document.createElement('audio');
        audioData = input.files[0];
        mt.controls = true;
        mt.src = url;
        $('#player')[0].innerHTML = "";
        $('#player').append(mt);
    };
    
    function checkValidity(file){
    	var isValid = false;
    	var allowedFileTypes = ['audio/x-wav', 'audio/wav', 'audio/mpeg', 'video/mp4' ];
    	isValid = allowedFileTypes.includes(file.type);
    	return isValid;
    }
    
    function displayError(errorMsg){
    	$('#error-panel').addClass('alert-danger');
        $('#error-message').text(errorMsg);
        $('#error-panel').show();
    }

    $(window).on('load',function(){
    	$("#file").val("");
    	$("#file").change(openFile);
    });

