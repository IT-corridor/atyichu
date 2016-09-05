var QBApp = {
    appId: 46077,
    authKey: 'F9FMK5hzzPsuO26',
    authSecret: 'uApjQ6BZrPg-Gcq'
};

var config = {
    chatProtocol: {
        active: 2
    },
    debug: {
        mode: 1,
        file: null
    },
    stickerpipe: {
        elId: 'stickers_btn',

        apiKey: '847b82c49db21ecec88c510e377b452c',

        enableEmojiTab: false,
        enableHistoryTab: true,
        enableStoreTab: true,

        userId: null,

        priceB: '0.99 $',
        priceC: '1.99 $'
    }
};

var currentUser = {
    login: 'user_b',
    pass: 'newfirst',
    full_name: 'User B'
};

QB.init(QBApp.appId, QBApp.authKey, QBApp.authSecret, config);
