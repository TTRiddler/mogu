$( document ).ready(function() {

    $('.trigger').click(function() {
        $('#modal-login').toggleClass('open');
    });

    $('.trigger3').click(function() {
        $('#modal-register').toggleClass('open');
        $('#modal-login').removeClass('open');
    });

    $('.trigger-phone').click(function() {
        $('#modal-phone').toggleClass('open');
    });

    $('.phone').mask("8 (999) 999-99-99");

    $('#user-name').click(function(){
        $('#profile-links').toggleClass('d-none');
    });

    $('#an-type-link .an-link-1').click(function(){
        $('.an-tab-1').fadeIn();
        $('.an-tab-2').css('display','none');
        $('#an-type-link .an-link-1').addClass('an-active-link');
        $('#an-type-link .an-link-2').removeClass('an-active-link');
    });

    $('#an-type-link .an-link-2').click(function(){
        $('.an-tab-2').fadeIn();
        $('.an-tab-1').css('display','none');
        $('#an-type-link .an-link-2').addClass('an-active-link');
        $('#an-type-link .an-link-1').removeClass('an-active-link');
    });

    $('.an_types_all>ul li i').click(function(){
        $(this).siblings('ul').toggleClass('d-none');
        $(this).toggleClass('fa-caret-right');
        $(this).toggleClass('fa-caret-down');
    });

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
    });

    $('#select_service_type').on('change', function() {
        service_type_id = $(this).val();

		data = {
            service_type_id: service_type_id,
        }

		$.ajax({
			type: "GET",
			url: $(this).attr('data-url'),
            data: data,
			success: function(data) {
                service = $('#select_service');
                service.find('option').remove();
                for(i=0; i < data.services_id.length; i++){
                    service.append('<option value="'+ data.services_id[i] + '">' + data.services_name[i] + '</option>');
                }  
            }
		});
    });


    var ans = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('q'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch:  'search.json?q=%QUERY',
        remote: {
            url: 'search.json?q=%QUERY',
            wildcard: '%QUERY'
        }
    });

    $('#multiple-datasets .typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 1,
        limit: 10,
    },
    {
        name: 'ans_list_search',
        display: 'q',
        source: ans
    });
});