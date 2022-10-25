$(function() {
    
    var stt_id = '';
    var params = (new URL(window.location)).searchParams;
    stt_id = params.get("stt_id");
    
    if (stt_id == null) {
    	$('#btnJson').hide(); 
    	$('#btnSRT').hide();
        $('#btnCSV').hide();
    	$('#btnEditTranscription').hide();
    	$('#transcriptions-panel').hide();
    } else{
        $('#btnJson').show(); 
    	$('#btnSRT').show();
        $('#btnCSV').show();
    	$('btnEditTranscription').show();
    	$('#transcriptions-panel').show();
    }
    
    $('#btnStatus').hide();
    $('#error-panel').hide();
    $('#progress-panel').hide();
    $('#status-panel').hide();
    
});

