const debug = require("debug")("botkit:domains");
const { BotkitConversation } = require("botkit");
const request = require("request-promise");
const schedule = require('node-schedule');

const resp = require("../response/response.js");

const CONVERSATION_MANAGER_ENDPOINT = "http://localhost:5000/api/send-message";
var MongoClient = require('mongodb').MongoClient;

var url = "mongodb+srv://chatbot:tmtchatbot@cluster0.jj9cp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
const fs = require("fs");
const limits = new Map();

var UserState = {};
var AdminState = {};
const pLimit = require('p-limit');
const { False, c } = require("../response/response.js");

require("dotenv").config({
  path: `../.env`,
})
var ip = process.env.IP_BACKEND
var port_backend = process.env.PORT_BACKEND

// var url = "http://" + ip + ':' + port_backend+"/api/send_message";
// var image_url = "http://" + ip + ':' + port_backend+"/api/send_image";

// var url = 'http://103.113.83.31:5050/api/send-message' ;
// var url = 'http://172.28.0.23:35077/get'
var url = 'http://127.0.0.1:5060/api/send_message'
var image_url = 'http://127.0.0.1:5060/api/send_image';
var message_queue = {};
var id_job_js = {};
var image_queue = {};
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function callMessageAPI(options, message, bot) {

  // async function impl (options,message,bot){
  const ref = message.reference;
  await bot.changeContext(ref);
  if ((message.user) in message_queue && message.text) {
    message_queue[message.user].push(message.text);
  }
  else if (message.text) {
    message_queue[message.user] = [message.text];
  }

  // if ((message.user) in image_queue && message.image ){
  //   image_queue[message.user].push(message.image.split(',')[1]);
  // }
  // else if (message.text){
  //   message_queue[message.user] = [message.text];
  // }

  // if (message.image){
  //   image_queue[message.user] = message.image;
  // }

  var jobList = schedule.scheduledJobs;
  var send_time = new Date().addSeconds(1);
  console.log("SEND TIME");
  console.log(send_time);
  var job = 'jobList.SendingSpan' + String(id_job_js[message.user]);
  if (eval(job) != undefined) {
    eval(job + '.cancel()')
  };
  const tmp_schedule = schedule.scheduleJob('SendingSpan' + String(id_job_js[message.user]), send_time, async function (bot, message) {
    message_queue[message.user] = [];
    image_queue[message.user] = '';
    async function impl(options, message, bot) {
      const ref = message.reference;
      await bot.changeContext(ref);
      await request(options, async function (error, response) {
        if (error) throw new Error(error);
        suggest_reply = JSON.parse(response.body)["suggest_reply"];
        id_job = JSON.parse(response.body)["id_job"];
        check_end = JSON.parse(response.body)["check_end"];
        rep_intent = JSON.parse(response.body)["rep_intent"];
        if (id_job && suggest_reply) {
          var job = 'jobList.RemindMess' + (id_job);
          if (eval(job) != undefined) {
            eval(job + '.cancel()')
          };
          // if(!check_end) {
          //   time_date = new Date().addMinutes(60);
          //   const tmp = schedule.scheduleJob('RemindMess'+id_job, time_date,function (bot,message){
          //   var remind_mes = "Em ngồi chờ mình mãi không thấy rep lại em" +
          //   "*Mình được kiểm hàng thoải mái. Nếu chất vải không đẹp, màu không y hình, chỉ may không tốt, form không đẹp trả lại em nha" +
          //   "*Chị lấy 1 váy làm duyên với shop e chị nha ^^";
          //   for (var sentence of remind_mes.split("*")){
          //     bot.reply(message, sentence);
          //   }
          //     tmp.cancel();
          //   }.bind(null,bot,message));

          // }

          if (suggest_reply && rep_intent !== undefined && rep_intent.includes("rep_inform")) {
            product_name = JSON.parse(response.body)["product_name"];
            color = JSON.parse(response.body)["color"];
            size = JSON.parse(response.body)["size"];
            amount = JSON.parse(response.body)["amount"];
            price = JSON.parse(response.body)["price"];
            chosenIdx = JSON.parse(response.body)["chosenIdx"];
            voucher = JSON.parse(response.body)["voucher"];
            ship_work_hour = JSON.parse(response.body)['ship_work_hour'];
            var sentence = suggest_reply.split("*");
            // Thông tin đơn hàng của chị là : 1 đầm caro màu xanh size S*
            // Sđt: 0905983795*
            // Địa chỉ 234 Bạch Đằng Phường 24 Quận Bình Thạnh Thành phố Hồ Chí Minh*
            // Phí ship tầm 20k nha chị iu*
            // Tầm 1-2 hôm chị nhận được hàng ạ*
            // Được kiểm tra hàng trước khi nhận ạ*
            // chị kiểm tra thông tin hộ shop nha
            var demo = {};
            var products = [];
            for (let index = 0; index < chosenIdx.length; index++) {
              // products[index] = {"name": product_name[chosenIdx[index]], "color": color[chosenIdx[index]], "size": size[chosenIdx[index]], "amount": amount[index], "price": price[chosenIdx[index]]};
              const idx_product = product_name.indexOf(chosenIdx[index])
              products[index] = { "name": chosenIdx[index], "color": color[idx_product], "size": size[idx_product], "amount": amount[idx_product], "price": price[idx_product] };
            }
            // console.log(products);
            demo['products'] = products;
            var today = new Date();
            var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            demo['date'] = date + ' ' + time;
            var count = 0;
            var text = '';
            if (sentence.length == 8) {
              count = 1;
              text = sentence[0] + ' Chị xác nhận lại đơn hàng giúp em nhé';
            }
            else {
              text = 'Chị xác nhận lại đơn hàng giúp em nhé'
            }
            demo['address'] = sentence[2 + count] + ". " + sentence[1 + count] // Địa chỉ ... Sđt ...	
            fee = sentence[3 + count].split(" ")[3]; // 20k	
            demo['fee'] = parseFloat(fee.substring(0, fee.length - 1));
            demo['ship_work_hour'] = ship_work_hour;
            demo['voucher'] = voucher;

            bot.reply(message, {
              text: text,
              demo: demo,
            });
            if (sentence.length > 5) {
              // await sleep(1500);	
              for (var sentence of [sentence[4 + count], sentence[5 + count]]) {
                bot.reply(message, sentence);
                // await sleep(1500);
              }
            }
          }
          else {
            for (var sentence of suggest_reply.split("*")) {
              bot.reply(message, sentence);
              // await sleep(1500);
            }
          }
        }

      });
      tmp_schedule.cancel();
    }

    const { id } = message.user // or similar to distinguish them

    if (!limits.has(id)) {
      limits.set(id, pLimit(1)); // only one active request per user
    }

    const limit = limits.get(id);
    return limit(impl, options, message, bot); // schedule impl for execution

  }.bind(null, bot, message));

  // }

  // const { id } = message.user // or similar to distinguish them

  // if (!limits.has(id)) {
  //   limits.set(id, pLimit(1)); // only one active request per user
  // }

  // const limit = limits.get(id);
  // return limit(impl, options,message,bot); // schedule impl for execution

}

defaultUserState = (ref) => ({
  subscriber: [],
  ref: ref,
});

defaultAdminState = (ref) => ({
  subscriber: [],
  ref: ref,
});

function s4() {
  // GENERATE RANDOM ID
  return Math.floor((1 + Math.random()) * 0x10000)
    .toString(16)
    .substring(1);
}

function createUserState(m) {
  for (let u in UserState) {
    if (m.user === u) {
      return UserState[u];
    }
  }
  return defaultUserState(m.reference);
}

function createAdminState(m) {
  for (let u in AdminState) {
    if (m.user === u) {
      return AdminState[u];
    }
  }
  return defaultAdminState(m.reference);
}

function getUserState(m) {
  for (let u in UserState) {
    if (m === u) {
      return UserState[u];
    }
  }
  return null;
}

function getAdminState(m) {
  for (let u in AdminState) {
    if (m === u) {
      return AdminState[u];
    }
  }
  return null;
}



module.exports = function (controller) {
  // controller.middleware.receive.use(rasa.receive);

  const onMessage = async (bot, message) => {
    var suggest_reply = '';
    var id_job = '';
    if (!(message.user in id_job_js)) {
      id_job_js[message.user] = Object.keys(id_job_js).length + 1;
    }
    if (message.image || (message.user in image_queue && image_queue[message.user])) {
      // console.log(message.image);
      if (message.user in message_queue && message_queue[message.user].length > 0) {
        var mess_text = message_queue[message.user].join('.') + "." + message.text;
      }
      else if (message.text)
        var mess_text = message.text;
      else
        var mess_text = '';

      if (message.user in image_queue && image_queue[message.user].length > 0 && message.image) {
        for (var img of message.image) {
          image_queue[message.user].push(img.split(',')[1]);
        }
        var list_image = image_queue[message.user];
      }
      else if (message.image) {
        var list_image = [];
        image_queue[message.user] = [];
        for (var img of message.image) {
          list_image.push(img.split(',')[1]);
          image_queue[message.user].push(img.split(',')[1]);
        }
      }
      else
        var list_image = image_queue[message.user];
      console.log("LENGTH OF IMAGE QUEUE");
      console.log(image_queue[message.user].length);

      // if (message.image){
      //   // console.log("MESSAGE IMAGE");
      //   // console.log(message.image);
      //   // console.log(typeof message.image);
      //   message.image = message.image.split(',')[1];
      // }
      // else{
      //   message.image = image_queue[message.user];
      // }
      var tmp = '';
      for (var v = 0; v < image_queue[message.user].length; v++) {
        if (v == image_queue[message.user].length - 1) {
          tmp += image_queue[message.user][v]
        }
        else {
          tmp += image_queue[message.user][v] + ',';
        }
      }



      console.log("----------BASE64 của ảnh--------");
      var options = {
        'method': 'POST',
        'url': image_url,
        'headers': {},
        formData: {
          'sender_id': message.user,
          'recipient_id': 'admin',
          'mid': s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4(),
          'image[]': tmp,
          'name': 'hume_products',
          'text': mess_text
        }
      };

      callMessageAPI(options, message, bot);

    }
    else {
      if (message.user in message_queue && message_queue[message.user].length > 0) {
        var mess_text = message_queue[message.user].join('.') + "." + message.text;
      }
      else
        var mess_text = message.text;

      var options = {
        'method': 'POST',
        'url': url,
        'headers': {},
        formData: {
          'sender_id': message.user,
          'recipient_id': 'admin',
          'mid': s4() + s4() + "-" + s4() + "-" + s4() + "-" + s4() + "-" + s4() + s4() + s4(),
          'text': mess_text,
          'name': 'hume_products'
        }
      };
      // while (true){
      //   console.log(UserState[message.user+'check_respones']);
      //   if (UserState[message.user+'check_respones']) break;
      // };
      // console.log("GỬI nè");
      // UserState[message.user+'check_respones'] = false;
      callMessageAPI(options, message, bot);
      // await request(options, function (error, response) {
      //   if (error) throw new Error(error);``
      //   suggest_reply = JSON.parse(response.body)["suggest_reply"];
      //   id_job = JSON.parse(response.body)["id_job"];
      // });

      //check if job exists
      // var jobList = schedule.scheduledJobs;
      // // console.log("JOBLIST")
      // // console.log(jobList);
      // // console.log(typeof id_job);
      // // console.log(id_job);
      // if (id_job && suggest_reply){
      //   var job = 'jobList.RemindMess' + (id_job);
      //   if (eval(job) != undefined){
      //     eval(job +'.cancel()')};
      //   time_date = new Date().addMinutes(2);
      //   console.log("TIMEEE");
      //   console.log(time_date);
      //   const ref = message.reference;
      //   await bot.changeContext(ref);
      //   const tmp = schedule.scheduleJob('RemindMess'+id_job, time_date,function (bot,message){
      //   var remind_mes = "Em ngồi chờ mình mãi không thấy rep lại em" +
      //   "*Mình được kiểm hàng thoải mái. Nếu chất vải k đẹp, màu k y hình, chỉ may k tốt, form k đẹp trả lại e nha" +
      //   "*Chị lấy 1 váy làm duyên với shop e chị nha ^^";
      //   for (var sentence of remind_mes.split("*")){
      //     bot.reply(message, sentence);
      //   }
      //     //console.log("REPPPPPPP");
      //     tmp.cancel();
      //   }.bind(null,bot,message));

      //   // set scheduler for reply text 
      //   var job = 'jobList.ReplyMess' + (id_job);
      //   if (eval(job) != undefined){
      //     eval(job +'.cancel()')};
      //   time_date = new Date().addSeconds(30);
      //   console.log("REPLY TIME");
      //   console.log(time_date);
      //   await bot.changeContext(ref);
      //   const tmp_reply = schedule.scheduleJob('ReplyMess'+id_job, time_date,function (bot,message,suggest_reply){
      //   for (var sentence of suggest_reply.split("*")){
      //     bot.reply(message, sentence);
      //   }
      //     //console.log("REPPPPPPP");
      //     tmp_reply.cancel();
      //   }.bind(null,bot,message,suggest_reply));
      // }

      // if (suggest_reply){
      //   for (var sentence of suggest_reply.split("*")){
      //     bot.reply(message, sentence);
      //   }
      // }
    }


  };

  const onWelcomeBack = async (bot, message) => {
    debug("Welcome back");
    UserState[message.user] = await createUserState(message);
    UserState[message.user + 'check_respones'] = true;
    await bot.reply(message, "Xin chào, mình là TMT Intelligent Chatbot. Bạn cần mình giúp gì nè");
  };

  const onHelloClient = async (bot, message) => {
    debug("Welcome back");
    UserState[message.user] = await createUserState(message);
    UserState[message.user + 'check_respones'] = true;
    // for (let u in AdminState) {
    //   let subscribeState = getAdminState(u);
    //   subscribeState.subscriber.push(UserState[message.user].ref);
    //   return await bot.reply(
    //     message,
    //     "Bạn đã lắng nghe người dùng: " + u
    //   );
    // }


    await bot.reply(message, "Xin chào, mình là TMT Intelligent Chatbot. Bạn cần mình giúp gì nè");
  };

  const onHelloAdmin = async (bot, message) => {
    AdminState[message.user] = await createAdminState(message);
    await bot.reply(message, "Xin chào admin");
    let reply = [];

    for (let u in UserState) {
      reply.push({
        title: u,
        payload: `subscribe ${u}`,
      });
    }
    await bot.reply(message, {
      text: "Hệ thống hiện có các khách hàng sau",
      quick_replies: reply,
    });
  };

  const onAdminMessage = async (bot, message) => {
    console.log(message.text);
  }

  controller.on("welcome_back", onWelcomeBack);
  controller.on("hello", onWelcomeBack);
  controller.on("client_hello", onHelloClient);
  // controller.on("image", onImage);
  controller.on("message", onMessage);
  controller.on("admin_hello", onHelloAdmin);
  controller.on("admin_message", onAdminMessage);
  // controller.on("image", imageProcess);
};
