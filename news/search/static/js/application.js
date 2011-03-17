$('a[data-delete=true]').click(function(event) {
	if(!confirm('Are you sure you want to delete this ' + $(this).attr('data-type') + '?'))
		event.preventDefault();
});

$('li.toggle').click(function(event) {
	if($(this).hasClass('show_all')) {
		$(this).removeClass('show_all');
		$(this).addClass('hide');
		$(this).html('Hide');
		$(this).parents('.briefing').find('.extra_stories').slideDown();
	} else {
		$(this).addClass('show_all');
		$(this).removeClass('hide');
		$(this).html('Show All');
		$(this).parents('.briefing').find('.extra_stories').slideUp();
	}
	
	event.preventDefault();
});


$('li.edit > a').click(function(event) {
	if($(this).hasClass('show')) {
		$(this).removeClass('show');
		$(this).addClass('hide');
		$(this).parents('.edit').find('.query_list').fadeIn();
	} else {
		$(this).addClass('show');
		$(this).removeClass('hide');
		$(this).parents('.edit').find('.query_list').fadeOut();
	}
	
	event.preventDefault();
});


$('li.edit .query_list form a').click(function(event) {
	$(this).parents('.edit').find('.btn').addClass('show');
	$(this).parents('.edit').find('.btn').removeClass('hide');
	$(this).parents('.edit').find('.query_list').fadeOut();
	event.preventDefault();
});
