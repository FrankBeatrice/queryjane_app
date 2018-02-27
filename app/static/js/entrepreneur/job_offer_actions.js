$(function () {
    // CLose job offer.
    $('.job_offer_close_link').on('click', function () {
        var job_link = $(this);
        var job_id = job_link.data('job-offer-id');
        var close_job_url = job_link.data('close-job-url');

        $.confirm({
            title: 'Do you want to close this job offer?',
            content: 'Users will not be able to apply and you will not be able to activate it again.',
            buttons: {
                close: {
                    btnClass: 'btn-danger',
                    action: function(){
                        $.post(close_job_url, function (response) {
                            if (response === 'success') {
                                $('.jsJobDetailActions').remove();
                                $('.JODetailStatus').removeClass('label-success').addClass('label-warning').text('Closed');
                            }
                        });
                    }
                },
                cancel: function () {}
            }
        });
    });
})
