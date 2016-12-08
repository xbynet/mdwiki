$(function(){
	$('.button-checkbox').each(function(){
		var $widget = $(this),
		$button = $widget.find('button'),
		$checkbox = $widget.find('input:checkbox'),
		color = $button.data('color'),
		settings = {
			on: {
				icon: 'glyphicon glyphicon-check'
			},
			off: {
				icon: 'glyphicon glyphicon-unchecked'
			}
		};

		$button.on('click', function () {
			$checkbox.prop('checked', !$checkbox.is(':checked'));
			$checkbox.triggerHandler('change');
			updateDisplay();
		});

		$checkbox.on('change', function () {
			updateDisplay();
		});

		function updateDisplay() {
			var isChecked = $checkbox.is(':checked');
			// Set the button's state
			$button.data('state', (isChecked) ? "on" : "off");

			// Set the button's icon
			$button.find('.state-icon')
			.removeClass()
			.addClass('state-icon ' + settings[$button.data('state')].icon);

			// Update the button's color
			if (isChecked) {
				$button
				.removeClass('btn-default')
				.addClass('btn-' + color + ' active');
			}
			else
			{
				$button
				.removeClass('btn-' + color + ' active')
				.addClass('btn-default');
			}
		}
		function init() {
			updateDisplay();
			// Inject the icon if applicable
			if ($button.find('.state-icon').length == 0) {
				$button.prepend('<i class="state-icon ' + settings[$button.data('state')].icon + '"></i> ');
			}
		}
		init();
	});
	
	$("#captcha").on('click',function(){
		var $img=$("#captcha");
		var src=$img.attr('src');
		var i=src.indexOf('?d=');
		if(i>0){
			src=src.substring(0,i);
		}
		var d=new Date();
		$img.attr('src',src+'?d='+d.getTime());
	});
	

	$("#loginForm").validate({
		submitHandler: function(form) {
			form.submit();
		},
		rules: {
			code:"required",
			password: "required",
			email: {
				required: true,
				email: true
			}
		},
		messages: {
			code: "必填",
			password: "必填",
			email: {
				required: "必填",
				email: "必须是email格式"
			}
		}
	});
});