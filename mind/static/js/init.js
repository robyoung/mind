(function($){
  $(function(){

    $('.button-collapse').sideNav();

    $('.answer').click(function(event) {
      let answer_elem = $('#answer-form input[name=answer]');
      answer_elem.val(event.currentTarget.dataset.answer);
      let answer_form = $('#answer-form');
      answer_form.submit()
      event.preventDefault();
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space
