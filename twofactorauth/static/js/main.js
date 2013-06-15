$("document").ready(function() {
	//////////////////////////////////
	// event handlers registration  //
	//////////////////////////////////
	$(".phone-number").keyup(function(e) {
		phoneNumber = $(this).val();
	});

	$(".phone-number-verify-button").click(function(e) {
		$.ajax({
			"url": "/verify/" + phoneNumber,
			"type": "GET",
			"success": function(data) {
				if(data["status"] == "success") {
					// show the verification code input box
					$(".code-row").css({"display": "block"});
				}
			},
			"error": function() {
				// error
			}
		});
	});

	$(".verification-code-check-button").click(function(e) {
		$.ajax({
			"url": "/checkcode/" + phoneNumber + "/" + $(".verification-code").val(),
			"type": "GET",
			"success": function(data) {
				if(data["status"] == "success") {
					$(".result-row h2").removeClass("notok");
					$(".result-row h2").addClass("ok");
					$(".result-row h2").html("Verified!");
				} else {
					$(".result-row h2").removeClass("ok");
					$(".result-row h2").addClass("notok");
					$(".result-row h2").html("Not Verified!");
				}

				$(".result-row").css({"display": "block"});
			},
			"error": function() {
				// error
			}
		});
	});
});