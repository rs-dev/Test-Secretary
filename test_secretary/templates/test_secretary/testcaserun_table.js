<script>
    function set_testcaserun_status(elemid, stat) {
        var td = $('#status'+elemid);
        var btn_vis = td.find('button.shown');
        var btn_hid = td.find('button.hidden');
        var href = btn_vis.attr('href');
        var span = td.find('span.state-label');
        $.get(href, success=function resp(data){
            btn_vis.removeClass('shown');
            btn_vis.addClass('hidden');
            btn_hid.removeClass('hidden');
            btn_hid.addClass('shown');
            if(stat=='OK') {
                span.removeClass('label-default');
                span.addClass('label-success');
                span.text('success');
            } else {
                span.removeClass('label-success');
                span.addClass('label-default');
                span.text('untested');
            }
        });
    }
</script>
