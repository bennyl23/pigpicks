$( document ).ready(function() {
	// use jquery datatables plugin on the league picks table
	$('#league_picks_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": true,
		"aaSorting": [[ 0, "asc"]],
		"aoColumns": [null, null, null, null, null, null, null, null, null],
		"aoColumnDefs": [{
			'bSortable': false,
			'aTargets': [4]
		}]
	});

	// use jquery datatables plugin on the week breakdown table
	$('#week_breakdown_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": true,
		"aaSorting": [[ 1, "desc"]],
		"aoColumns": [null, null]
	});

	// use jquery datatables plugin on the standings table
	$('#standings_table').dataTable({
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bSort": true,
        "bInfo": false,
        "bAutoWidth": false,
		"bProcessing": true,
		"aaSorting": [[ 2, "desc"]],
		"aoColumns": [null, null, null, null],
		"aoColumnDefs": [{
			'bSortable': false,
			'aTargets': [0,3]
		}]
	});

	$("#best_bet_info").popover();
});

togglePickButton = function(btnNum, nfl_team_id, matchup_id){
	var btn = $("#btn" + matchup_id + '_' + btnNum);
	if (btn.hasClass("active")){
		// remove the focus when button becomes inactive
		btn.blur();
		// button is inactive, clear the matchup
		clearMatchupInput(matchup_id);
	}
	else{
		// button is active, set the matchup
		setMatchupInput(matchup_id, nfl_team_id);
	}
	btn.toggleClass("active");

	if (btnNum == '1'){
		var btnOther = $("#btn" + matchup_id + "_2");
	}
	else{
		var btnOther = $("#btn" + matchup_id + "_1");
	}
	// toggle the other button in the matchup if it's active
	if (btnOther.hasClass("active")){
		btnOther.removeClass("active");
	}
}

setMatchupInput = function(matchup_id, nfl_team_id){
	var matchupInput = $("#" + matchup_id);
	matchupInput.val(nfl_team_id);
}

clearMatchupInput = function(matchup_id){
	var matchupInput = $("#" + matchup_id);
	matchupInput.val('0');
}