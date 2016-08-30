/*
    Notification for wechat.
    It uses toastr hints to display notificaitons.
 */

var pusher = new Pusher('4c8e6d909a1f7ccc44ed');
var notificationsChannel = pusher.subscribe('nf_channel_'+user_id);

notificationsChannel.bind('new_notification', function(notification){
    var message = notification.message;
    toastr.success(message);

    $('#id_nf_group').prepend('<div class="well">'+message+'</div>');
});
