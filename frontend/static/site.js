$(document).ready(function() {
  $('.helper-row').on('click', '.adder', function(event) {
    $.ajax({
      method: "GET",
      url: $(this).attr('href')
    })
      .fail(function() {
        console.log("error");
      })
      .done(function(msg) {
        var in_list = $(event.target).parents('li');
        if (in_list.length > 0) {
          in_list.hide();
        } else {
          $(event.target).parents('.helper-row').html(msg.content);
        }
      });
    return false;
  });
})
