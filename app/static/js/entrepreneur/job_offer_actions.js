$(function () {
    // CLose job offer.
    $('.job_offer_close_link').on('click', function () {
        var job_link = $(this);
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
                                job_link.closest('.JOContainer').find('.JODetailStatus').removeClass('label-success').addClass('label-warning').text('Closed');
                                job_link.closest('.JOContainer').find('.jsJobActions').remove();
                            }
                        });
                    }
                },
                cancel: function () {}
            }
        });
    });
})
