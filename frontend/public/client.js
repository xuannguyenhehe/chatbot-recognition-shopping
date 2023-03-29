var converter = new showdown.Converter();
converter.setOption("openLinksInNewWindow", true);
var index = 0;

var Botkit = {
    userID: "",
    historyChat: "",
    tthc_id: null,
    config: {
        ws_url:
            (location.protocol === "https:" ? "wss" : "ws") +
            "://" +
            location.host,
        reconnect_timeout: 3000,
        max_reconnect: 5,
    },
    options: {
        sound: false,
        use_sockets: true,
    },
    reconnect_count: 0,
    guid: null,
    current_user: null,
    on: function (event, handler) {
        this.message_window.addEventListener(event, function (evt) {
            handler(evt.detail);
        });
    },
    trigger: function (event, details) {
        var event = new CustomEvent(event, {
            detail: details,
        });
        this.message_window.dispatchEvent(event);
    },
    reset: function () {
        var that = this;
        that.tthc_id = null;
        that.deliverMessage({
            type: "reset",
        });
    },
    clear: function () {
        var that = this;
        that.tthc_id = null;
    },
    request: function (url, body) {
        var that = this;
        return new Promise(function (resolve, reject) {
            var xmlhttp = new XMLHttpRequest();

            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                    if (xmlhttp.status == 200) {
                        var response = xmlhttp.responseText;
                        var message = null;
                        try {
                            message = JSON.parse(response);
                        } catch (err) {
                            reject(err);
                            return;
                        }
                        resolve(message);
                    } else {
                        reject(new Error("status_" + xmlhttp.status));
                    }
                }
            };

            xmlhttp.open("POST", url, true);
            xmlhttp.setRequestHeader("Content-Type", "application/json");
            xmlhttp.send(JSON.stringify(body));
        });
    },
    showHistoryChatChat: function () {
        return this.historyChat;
    },
    showUserID: function () {
        return this.userID;
    },
    send: function (text, e) {
        var that = this;
        if (e) e.preventDefault();
        if (!text && !that.image) {
            return;
        }
        var message = {
            type: "outgoing",
            text: text,
            image: that.image,
        };
        this.clearReplies();
        if (text) {
            that.renderMessage(message);
        }
        // if (that.image) {
        //     that.renderImage(message)
        // }

        that.deliverMessage({
            type: "message",
            text: text,
            image: that.image,
            tthc_id: that.tthc_id,
            user: this.guid,
            channel: this.options.use_sockets ? "socket" : "webhook",
        });

        this.input.value = "";
        that.image = null;
        $("#image-label").text("");
        return false;
    },
    sendCustom: function (text, payload, e) {
        var that = this;
        if (e) e.preventDefault();
        if (!text) {
            return;
        }
        var message = {
            type: "outgoing",
            text: text,
        };

        this.clearReplies();
        that.renderMessage(message);

        that.deliverMessage({
            ...payload,
            type: "message",
            text: text,
            tthc_id: that.tthc_id,
            user: this.guid,
            channel: this.options.use_sockets ? "socket" : "webhook",
        });

        this.input.value = "";

        this.trigger("sent", message);

        return false;
    },
    sendCustomAction: function (text, payload, e) {
        var that = this;
        if (e) e.preventDefault();
        if (!text) {
            return;
        }
        var message = {
            type: "outgoing",
            text: text,
        };

        this.clearReplies();

        that.deliverMessage({
            ...payload,
            type: "message",
            text: text,
            user: this.guid,
            tthc_id: that.tthc_id,
            channel: this.options.use_sockets ? "socket" : "webhook",
        });

        this.input.value = "";

        this.trigger("sent", message);

        return false;
    },
    deliverMessage: function (message) {
        if (this.options.use_sockets) {
            this.socket.send(JSON.stringify(message));
        } else {
            this.webhook(message);
        }
    },
    connect: function (user) {
        var that = this;

        if (user && user.id) {
            Botkit.setCookie("botkit_guid", user.id, 1);

            user.timezone_offset = new Date().getTimezoneOffset();
            that.current_user = user;
            console.log("CONNECT WITH USER", user);
        }

        // connect to the chat server!
        if (that.options.use_sockets) {
            that.connectWebsocket(that.config.ws_url);
        }
    },
    connectWebsocket: function (ws_url) {
        var that = this;
        // Create WebSocket connection.
        that.socket = new WebSocket(ws_url);

        var connectEvent = "client_hello";
        // if (Botkit.getCookie("botkit_guid")) {
        //     that.guid = Botkit.getCookie("botkit_guid");
        //     connectEvent = "client_hello";
        // } else {
        //     that.guid = that.generate_guid();
        //     Botkit.setCookie("botkit_guid", that.guid, 1);
        // }
        that.guid = that.generate_guid();
        this.userID = that.guid
        console.log(that.guid)
        Botkit.setCookie("botkit_guid", that.guid, 1);

        // Connection opened
        that.socket.addEventListener("open", function (event) {
            // console.log('CONNECTED TO SOCKET');
            that.reconnect_count = 0;
            that.trigger("connected", event);
            that.deliverMessage({
                type: connectEvent,
                user: that.guid,
                tthc_id: that.tthc_id,
                channel: "socket",
                user_profile: that.current_user ? that.current_user : null,
            });


        });

        that.socket.addEventListener("error", function (event) {
            // console.error('ERROR', event);
        });

        that.socket.addEventListener("close", function (event) {
            // console.log('SOCKET CLOSED!');
            that.trigger("disconnected", event);
            if (that.reconnect_count < that.config.max_reconnect) {
                setTimeout(function () {
                    // console.log('RECONNECTING ATTEMPT ', ++that.reconnect_count);
                    that.connectWebsocket(that.config.ws_url);
                }, that.config.reconnect_timeout);
            } else {
                that.message_window.className = "offline";
            }
        });

        // Listen for messages
        that.socket.addEventListener("message", function (event) {
            var message = null;
            try {
                message = JSON.parse(event.data);
            } catch (err) {
                that.trigger("socket_error", err);
                return;
            }

            that.trigger(message.type, message);
        });
    },
    clearReplies: function () {
        console.log('oke')
    },
    quickReply: function (payload) {
        this.send(payload);
    },
    focus: function () {
        this.input.focus();
    },
    createNextLine: function () {
        var nextLine = document.createElement("li");
        nextLine.setAttribute("class", "ctext-wrap");
        return nextLine;
    },
    createNextLineImg: function () {
        var nextLine = document.createElement("li");
        nextLine.setAttribute("class", "right");
        return nextLine;
    },
    renderMessage: function (message) {
        let id = + new Date() +1
        var that = this;
        let hours = new Date().getHours()
        let minutes = new Date().getMinutes()
        if (message.isAbleToSuggest) {
            ableToSuggest = true;
        }

        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }

        if (message.text) {
            if (message.text == "Shop thời trang Hume") {
                message.text = "<a href=\"https://www.facebook.com/thoitranghume\"> Shop thời trang Hume </a>";
            }
            message.html = `<li id="`+id+`">
            <div class="chat-avatar-bot">
            <img src="image/bot_avatar.png"  class="rounded-circle avatar-sm">
        </div>
            <div class="conversation-list">
                <div class="ctext-wrap">

                    <p class="item_message item_message_bot">
                        `+message.text+`
                    </p>
                    <p class="chat-time mb-0"><i class="bx bx-time-five align-middle me-1"></i>`+hours+`:`+(minutes > 9 ? minutes:`0`+minutes)+`</p>
                </div>
            
                
            </div>
        </li>`
         }
        var re = new RegExp("image ");
        if (re.test(message.text)) {

            // var string_byte = message.text.replace("image ",'');
            // var imgElement = document.createElement("img");
            // // imgElement.src = "data:image/png;base64," + string_byte
            // imgElement.src = "http://172.28.0.23:35432/api/file/Get-File-Local?guid=Hume_shop_D0013-hồng-0.jpg" 
            // imgElement.style="width: 100%";
            // message.html = imgElement.outerHTML;
            var string_byte = message.text.replace("image ", "");
            var string_byte = string_byte.replace("hume_products", "Hume");
            console.log("IN", string_byte);
            var imgElement = document.createElement("img");
            imgElement.className = "img-thumbnail item_message item_message_bot"
            imgElement.src = string_byte;
            // imgElement.src = "data:image/png;base64," + string_byte
            // imgElement.src = "http://172.28.0.23:35432/api/file/Get-File-Local?guid=Hume_shop_D0013-hồng-0.jpg" 
            imgElement.style = "width: 50%";
            message.text = imgElement.outerHTML;
            message.html = `<li id="`+id+`">
            <div class="chat-avatar-bot">
            <img src="image/bot_avatar.png"  class="img-thumbnail rounded-circle avatar-sm">
        </div>
            <div class="conversation-list">
                <div class="ctext-wrap">
                    
                
                        `+message.text+`
                    
                    <p class="chat-time mb-0"><i class="bx bx-time-five align-middle me-1"></i>`+hours+`:`+(minutes > 9 ? minutes:`0`+minutes)+`</p>
                </div>
            
                
            </div>
        </li>`
            
            //var base64String = btoa(String.fromCharCode.apply(null, new Uint8Array(string_byte)));
            //message.html = "<img src=\"data:image/png;base64," + string_byte +"\" width=\"400px\" height=\"300px\" >";
        }

        const messageNode = that.message_template({
            message: message,
        });

        that.next_line.innerHTML = messageNode;
        // const boxStyler = styler(that.next_line);
        // if (boxStyler != null) {
        //     tween({
        //         from: { y: 100, scale: 0.1 },
        //         to: { y: 0, scale: 1.0 },
        //         ease: easing.backOut,
        //         duration: 500,
        //     }).start((v) => boxStyler.set(v));
        // }
        if(message.type !== 'outgoing'){
        that.message_list.appendChild(that.next_line);
        document.getElementById(id).scrollIntoView();
        var audio = new Audio("audio/sound.mp3");
        audio.play();
        }else{
        var audio = new Audio("audio/send.mp3");
        audio.play();
        }

        animateTyping();
        if (!message.isTyping) {
            delete that.next_line;
        }
    },
    renderImage: function (message) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLineImg();
        }
        if (message.image) {
            if (message.image.length == 1) {
                var imgElement = document.createElement("img");
                imgElement.className = 'img-thumbnail';
                imgElement.src = message.image;
                imgElement.style = "width: 50%"; 
                message.html = imgElement.outerHTML;
            }
            else if (message.image.length == 2) {
                var table = document.createElement('table');
                table.style = "border: hidden"
                table.innerHTML = `<tr>
                <td><img src=${message.image[0]} style="display:block;" width="100px" height="100px"></td>
                <td><img src=${message.image[1]} style="display:block;" width="100px" height="100px"></td>
                </tr>`;
                message.html = table.outerHTML;
            }
            else if (message.image.length == 3) {
                var table = document.createElement('table');
                table.style = "border: hidden"
                table.innerHTML = `<tr>
                    <td rowspan ="2"><img src=${message.image[0]} style="display:block;" width="100px" height="100px"></td>
                    <td><img src=${message.image[1]} style="display:block;" width="100px" height="100px"></td>
                </tr>
                <tr>
                    <td><img src=${message.image[2]} style="display:block;" width="100px" height="100px"></td>
                </tr>`;
                message.html = table.outerHTML;
            }
            else if (message.image.length == 4) {
                var table = document.createElement('table');
                table.style = "border: hidden"
                table.innerHTML = `<tr>
                    <td><img src=${message.image[0]} style="display:block;" width="100px" height="100px"></td>
                    <td><img src=${message.image[1]} style="display:block;" width="100px" height="100px"></td>
                </tr>
                <tr>
                    <td><img src=${message.image[2]} style="display:block;" width="100px" height="100px"></td>
                    <td><img src=${message.image[3]} style="display:block;" width="100px" height="100px"></td>
                </tr>`;
                message.html = table.outerHTML;
            }
            else {
                var table = document.createElement('table');
                table.style = "border: hidden"
                table.innerHTML = `<tr>`
                for (var img of message.image) {
                    table.innerHTML = table.innerHTML.concat(`<td><img src=${img} style="display:block;" width="100px" height="100px"></td>`)
                }
                table.innerHTML = table.innerHTML.concat(`</tr>`);
                message.html = table.outerHTML;
            }
        }
        const messageNode = that.message_template({
            message: message,
        });
        that.next_line.innerHTML = messageNode;
        
        that.historyChat = this.historyChat.concat("\n" + messageNode);
        that.message_list.appendChild(that.next_line);
        animateTyping();
        if (!message.isTyping) {
            delete that.next_line;
        }
    },
    renderAsk: function () {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        if (text === null) return;
        resp = converter.makeHtml(text);

        const messageNode = that.message_template({
            message: { html: text },
        });
        that.next_line.innerHTML = messageNode;

        // const boxStyler = styler(that.next_line);
        // if (boxStyler != null) {
        //     tween({
        //         from: { y: 100, scale: 0.1 },
        //         to: { y: 0, scale: 1.0 },
        //         ease: easing.backOut,
        //         duration: 500,
        //     }).start((v) => boxStyler.set(v));
        // }

        that.message_list.appendChild(that.next_line);

        animateTyping();
        if (!message.isTyping) {
            delete that.next_line;
        }
    },
    renderOptions: function (options) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        res = document.createElement("div");
        options.forEach((v, i) => {
            wrapper = document.createElement("div");
            button = document.createElement("button");
            button.className = "btn btn-success btn-px";
            text1 = document.createTextNode(i + 1);
            text2 = document.createTextNode(v.value);
            button.appendChild(text1);
            wrapper.appendChild(button);
            wrapper.appendChild(text2);
            res.appendChild(wrapper);
        });
        const messageNode = that.message_template({
            message: {
                html: res.innerHTML,
            },
        });
        that.next_line.innerHTML = messageNode;
        Array.from(that.next_line.childNodes[1].children).forEach((e, i) => {
            e.childNodes[0].addEventListener("click", () => {
                that.tthc_id = options[i].key;
                that.deliverMessage({
                    type: "message",
                    tthc_id: options[i].key,
                    tthc_name: options[i].value,
                    select: true,
                });
            });
        });
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },
    renderChiPhi: function (prices) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        var list_row =
            '<tr><th class="sotien">Số Tiền</th><th class="mota">Mô Tả</th></tr>';

        for (var v of prices) {
            list_row += `<tr><td>${v.SoTien ? v.SoTien : "Không Mất Phí"
                }</td><td>${v.MoTa ? v.MoTa : ""}</td></tr>`;
        }

        if (prices.length == 0) {
            list_row += `<tr><td>${"Không Mất Phí"}</td><td>${""}</td></tr>`;
            return;
        }

        var table = `<table class="chiphi">${list_row}</table>`;

        const messageNode = that.message_template({
            message: {
                html: table,
                type: "scroll",
            },
        });
        that.next_line.innerHTML = messageNode;
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },

    renderThoiGian: function (v) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        res = document.createElement("div");
        ul = document.createElement("ul");
        ul.className = "ul";
        li1 = document.createElement("li");
        text1 = document.createTextNode(
            `Mô tả: ${v.MoTa ? v.MoTa : "Không có dữ liệu"}`
        );
        li1.appendChild(text1);
        li2 = document.createElement("li");
        text2 = document.createTextNode(
            `Thời gian giải quyết: ${v.ThoiGianGiaiQuyet ? v.ThoiGianGiaiQuyet : "Không có dữ liệu"
            }`
        );
        li2.appendChild(text2);
        li3 = document.createElement("li");
        text3 = document.createTextNode(
            `Đơn vị tính: ${v.DonViTinh ? v.DonViTinh : "Không có dữ liệu"}`
        );
        li3.appendChild(text3);
        ul.appendChild(li1);
        ul.appendChild(li2);
        ul.appendChild(li3);
        res.appendChild(ul);

        const messageNode = that.message_template({
            message: {
                html: res.outerHTML,
            },
        });
        that.next_line.innerHTML = messageNode;
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },
    renderKetQua: function (result) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        res = document.createElement("div");
        ul = document.createElement("ul");
        ul.className = "ul";
        result.forEach((v) => {
            li = document.createElement("li");
            text = document.createTextNode(`${v.MoTa}`);
            li.appendChild(text);
            ul.appendChild(li);
        });
        res.appendChild(ul);

        const messageNode = that.message_template({
            message: {
                html: res.outerHTML,
            },
        });
        that.next_line.innerHTML = messageNode;
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },
    renderDemo: function (demo) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        var sum = 0;

        var list_row = `<tr><th class="products">MẶT HÀNG</th></tr>`;
        for (var v of demo.products) {
            sum += v.price * v.amount;
            if (v.size === 'free_size')
            {
                list_row += `<tr><td style="width:700px">${v.amount} ${v.name} màu ${v.color} free size <br>Giá tiền: ${v.price * v.amount}</br></td></tr>`;
            }
            else
            {
                list_row += `<tr><td style="width:700px">${v.amount} ${v.name} màu ${v.color} size ${v.size}<br>Giá tiền: ${v.price * v.amount}</br></td></tr>`;
            }
            
        }
        sum += demo.fee
        // list_row += `<tr><td style="width:700px">${demo.products}</td></tr>`;
        list_row += `<tr><th class="date">NGÀY ĐẶT HÀNG</th></tr>`;
        list_row += `<tr><td style="width:700px">${demo.date}</td></tr>`;
        list_row += `<tr><th class="date">THANH TOÁN BẰNG</th></tr>`;
        list_row += `<tr><td style="width:700px">Thanh toán khi giao hàng (COD)</td></tr>`;
        list_row += `<tr><th class="date">VẬN CHUYỂN ĐẾN</th></tr>`;
        list_row += `<tr><td style="width:700px">${demo.address}</td></tr>`;
        list_row += `<tr><th class="date">PHÍ GIAO HÀNG</th></tr>`;
        list_row += `<tr><td style="width:700px">${demo.fee}</td></tr>`;
        list_row += `<tr><th class="date">TỔNG CỘNG</th></tr>`;
        list_row += `<tr><td style="width:700px">${sum}</td></tr>`;
        if (demo.voucher && 'detail' in demo.voucher) {
            var detail = demo.voucher['detail'];
            sum_voucher = demo.voucher['sum_price'];
            list_row += `<tr><th class="date">TỔNG CỘNG (khi áp dụng voucher</th></tr>`;
            list_row += `<tr><th class="date">${detail})</th></tr>`;
            list_row += `<tr><td style="width:700px">${sum_voucher}</td></tr>`;
        }
        if (demo.ship_work_hour) {
            list_row += `<tr><th class="date">LƯU Ý</th></tr>`;
            list_row += `<tr><td style="width:700px">Giao giờ hành chính</td></tr>`;
        }
        // var list_row = 
        //     '<tr><th class="product_name">Tên sản phẩm</th><th class="color">Màu sắc</th><th class="s">S</th><th class="m">M</th><th class="l">L</th><th class="xl">XL</th><th class="xxl">XXL</th><th class="price">Giá tiền</th></tr>';
        // for (var v of product_introduction) {
        //     list_row += `<tr ><td style="width:700px">${v.product_name}</td><td>${
        //         v.color ? v.color : "Chưa xác định"
        //     }</td><td>${
        //         v.S ? v.S : 0
        //     }</td><td>${
        //         v.M ? v.M : 0
        //     }</td><td>${
        //         v.L ? v.L : 0
        //     }</td><td>${
        //         v.XL ? v.XL : 0
        //     }</td><td>${
        //         v.XXL ? v.XXL : 0
        //     }</td><td>${
        //         v.price ? v.price : 0
        //     }</td></tr>`;


        //    <td><a href="${v.url ? v.url : "#"}">${
        //         v.url ? "Link" : ""
        //     }</a></td></tr>`;
        // }
        var table = `<table class="table">${list_row}</table>`;
        var nameId = "showhide" + index.toString();
        console.log(index);
        var button = `<input type="button" onclick="javascript:toggle(${index})" value="XÁC NHẬN ĐƠN ĐẶT HÀNG">
        <div id=${nameId} style="display: block">${table}</div>`;
        const messageNode = that.message_template({
            message: {
                html: button,
                type: "scroll",
            },
        });
        index += 1;
        console.log(index);

        that.next_line.innerHTML = messageNode;
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },
    renderThucHien: function (process) {
        var that = this;
        if (!that.next_line) {
            that.next_line = that.createNextLine();
        }
        res = document.createElement("div");
        ul = document.createElement("ol");
        ul.className = "ol";
        process.forEach((v) => {
            li = document.createElement("li");
            text = document.createTextNode(`${v.TenTrinhTu}`);
            li.appendChild(text);
            ul.appendChild(li);
        });
        res.appendChild(ul);

        const messageNode = that.message_template({
            message: {
                html: res.outerHTML,
            },
        });
        that.next_line.innerHTML = messageNode;
        that.message_list.appendChild(that.next_line);
        that.next_line = that.createNextLine();
    },
    triggerScript: function (script, thread) {
        this.deliverMessage({
            type: "trigger",
            user: this.guid,
            channel: "socket",
            tthc_id: that.tthc_id,
            script: script,
            thread: thread,
        });
    },
    identifyUser: function (user) {
        user.timezone_offset = new Date().getTimezoneOffset();

        this.guid = user.id;
        Botkit.setCookie("botkit_guid", user.id, 1);

        this.current_user = user;

        this.deliverMessage({
            type: "identify",
            user: this.guid,

            tthc_id: that.tthc_id,
            channel: "socket",
            user_profile: user,
        });
    },
    receiveCommand: function (event) {
        switch (event.data.name) {
            case "trigger":
                Botkit.triggerScript(event.data.script, event.data.thread);
                break;
            case "identify":
                Botkit.identifyUser(event.data.user);
                break;
            case "connect":
                Botkit.connect(event.data.user);
                console.log("event data user " + event.data.user);
                break;
            default:
        }
    },
    sendEvent: function (event) {
        if (this.parent_window) {
            this.parent_window.postMessage(event, "*");
        }
    },
    setCookie: function (cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
    getCookie: function (cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(";");
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == " ") {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    },
    generate_guid: function () {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return (
            s4() +
            s4() +
            "-" +
            s4() +
            "-" +
            s4() +
            "-" +
            s4() +
            "-" +
            s4() +
            s4() +
            s4()
        );
    },

    boot: function (user) {

        var that = this;

        that.message_window = document.getElementById("message_window");

        that.message_list = document.getElementById("message_list");

        var source = document.getElementById("message_template").innerHTML;
        that.message_template = Handlebars.compile(source);
        console.log(that.message_template);
        var custom_source = document.getElementById("message_slider_template")
            .innerHTML;


        that.input = document.getElementById("messenger_input");

        $("#image-icon").click(function () {
            $("#image-input").trigger('click');
        });

        $('#image-input').on('change', function () {
            _readFileDataUrl(this, function (err, files) {
                if (err) { return }
                for(let k=0;k<files.length;k++){
                $("#image_input").append('<img src="'+files[k]+'"  class="img-thumbnail" width="150"  style="margin-right:10px;max-height:150px">');
                    }
                $('#image_input').show()
                // $('#messenger_input').attr("disabled", true);
                stoppedTyping()
                //contains base64 encoded string array holding the 
                that.image = files;
            });
        });
        var _readFileDataUrl = function (input, callback) {
            var len = input.files.length, _files = [], res = [];
            var readFile = function (filePos) {
                if (!filePos) {
                    callback(false, res);
                } else {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        res.push(e.target.result);
                        readFile(_files.shift());
                    };
                    reader.readAsDataURL(filePos);
                }
            };
            for (var x = 0; x < len; x++) {
                _files.push(input.files[x]);
            }
            readFile(_files.shift());
        };

        that.focus();

        that.on("connected", function () {
            // that.message_window.className = "connected";
            that.input.disabled = false;
            that.sendEvent({
                name: "connected",
            });
        });

        that.on("disconnected", function () {
            that.message_window.className = "disconnected";
            that.input.disabled = true;
        });

        that.on("typing", function () {
            that.clearReplies();
            console.log("typing");
            that.renderMessage({
                isTyping: true,
            });
        });

        that.on("sent", function () {
            deleteElement();
            if (ableToSuggest != undefined) {
                ableToSuggest = false;
            }
            if (that.options.sound) {
                var audio = new Audio("audio/sound.mp3");
                audio.play();
            }
        });

        that.on("message", function () {
            if (that.options.sound) {
                var audio = new Audio("beep.mp3");
                audio.play();
            }
        });

        that.on("message", function (message) {
            if (message.choices) {
                that.renderMessage(message);
                that.renderOptions(message.choices);
            } else if (message.demo) {
                that.renderMessage(message);
                that.renderDemo(message.demo);
            } else if (message.chiphi) {
                that.renderMessage(message);
                that.renderChiPhi(message.chiphi);
            } else if (message.type === "response") {
                that.renderMessage(message);
            } else if (message.thuchien) {
                that.renderMessage(message);
                that.renderThucHien(message.thuchien);
            } else if (message.thoigian) {
                that.renderMessage(message);
                that.renderThoiGian(message.thoigian);
            } else if (message.goodbye) {
                that.renderMessage(message);
                that.clear();
            } else {
                that.renderMessage(message);
            }
        });

        if (window.self !== window.top) {
            that.parent_window = window.parent;
            window.addEventListener("message", that.receiveCommand, false);
            that.sendEvent({
                type: "event",
                name: "booted",
            });
        } else {
            that.connect(user);
        }

        return that;
    },
};

(function () {
    Botkit.boot();
})();

