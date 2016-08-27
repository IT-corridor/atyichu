/*
 Notification for wechat.
 It uses toastr hints to display notificaitons.
 */

var pusher = new Pusher('4c8e6d909a1f7ccc44ed');
var notificationsChannel = pusher.subscribe('nf_channel_' + user_id);

notificationsChannel.bind('new_notification', function (notification) {
    // show notification toaster
    var message = notification.message;
    toastr.success(message);
    // increase the notification number
    var nf_num = parseInt($('#id_nf_num').text(), 10);
    $('#id_nf_num').text(nf_num + 1);

    $('#id_nf_group').prepend('<a href class="list-group-item">\
                    <span class="clear block m-b-none">'
                      +notification.message + '<br>\
                      <small class="text-muted">notification</small>\
                    </span>\
                  </a>'
    );
});
