$(document).on('click', '#like', function(event){
  const ajaxUrl = $(this).attr("data-href");
  const csrfData = $(this).attr("data-csrf");
  console.log(csrfData);
  console.log(ajaxUrl);
  event.preventDefault();
  $.ajax({
      type: 'POST',
      url: ajaxUrl,
      data: {
          'post_id': $(this).attr('name'),
          'csrfmiddlewaretoken': csrfData
      },
      dataType: 'json',
      success: function(response){
          selector = document.getElementsByName(response.post_id);
          if(response.liked){
              $(selector).html("<i class='fas fa-lg fa-heart'></i>");
          }
          else {
              $(selector).html("<i class='far fa-lg fa-heart'></i>");
          }
          selector2 = document.getElementsByName(response.post_id + "-count");
          $(selector2).text(response.count);
      }
  });
});