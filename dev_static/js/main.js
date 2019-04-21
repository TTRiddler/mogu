$( document ).ready(function() {

    $('.trigger').click(function() {
        $('#modal-add-service').toggleClass('open');
    });

    $('.trigger1').click(function() {
        $('#modal-login').toggleClass('open');
    });

    $('.trigger3').click(function() {
        $('#modal-register').toggleClass('open');
        $('#modal-add-service').removeClass('open');
        $('#modal-login').removeClass('open');
    });

    $('.trigger-phone').click(function() {
        $('#modal-phone').toggleClass('open');
    });

    $('.phone').mask("8 (999) 999-99-99");

    $('.slider-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.slider-nav',
        cssEase: 'none',
    });
    
    $('.slider-nav').slick({
        slidesToScroll: 1,
        slidesToShow: 3,
        asNavFor: '.slider-for',
        arrows: false,
        dots: false,
        centerMode: true,
        focusOnSelect: true,
        rtl: false,
    });

    $('#add_new_an .files-add input[type="file"]').bind('change', function(){
        up_files = this.files;
        
        if (up_files.length > 10) {
            $('.files-add .file-add-res').html('<span style="color:red; font-size:0.9rem;">Слишком много фотографий</span>');
            up_files = {};
        } else {
            var files_name = '';
            for (var i=0; i<up_files.length; i++){
                files_name += '<p>' + up_files[i].name + '</p>';
            }
            $('.files-add .file-add-res').html(files_name);
        }
        console.log(up_files)
    });

});