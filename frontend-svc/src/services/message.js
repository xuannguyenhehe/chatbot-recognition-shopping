import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put, select } from "redux-saga/effects";
import { getURL, getFullURL } from "utils/url";

function* getMessages({ payload }) {
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isShowLoading: true,
        messages: null,
      },
    });
    let response = yield call(
      async () =>
        await API.get(getURL("message", "ENTRYPOINT"), {
          params: {
            chat_user: payload.chatUser,
          },
        }),
    );
    if (response.status === 200) {
      yield put({
        type: "message/saveState",
        payload: {
          messages: response.data.data.map((messageObj) => ({
            message: messageObj.message,
            image: messageObj.path_image
              ? getFullURL('image/' + messageObj.path_image, "ENTRYPOINT")
              : null,
            sender: messageObj.sender,
            receiver: messageObj.receiver,
            options: messageObj?.options?.length 
              ? messageObj.options.map((option) => getFullURL('image/' + option, "ENTRYPOINT")) 
              : null,
            is_option_action: messageObj?.is_option_action,
          })),
          isShowLoading: false,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "message/saveState",
      payload: {
        isShowLoading: false,
        messages: null,
      },
    });
  }
}

function* sendMessage({ payload }) {
  const state = yield select();
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: true,
      },
    });
    let body_image = null;
    let isForceSend = payload.isForceSend;
    if (payload.image) {
      body_image = {
        data: payload?.image.dataURL,
        filename: payload?.image.file.name,
      };
      isForceSend = true;
    }

    let messages = [...state.message.messages];
    let intent = null;
    let bodyIntent = {
      message: payload.message,
    };
    let responseIntent = yield call(
      async () => await API.post(getFullURL("answer/intent", "RASA"), bodyIntent),
    );
    if (responseIntent.status === 200) {
      intent = responseIntent.data.data.intent.name;
    }

    if ((intent === "ask_type" && isForceSend) || intent !== "ask_type") {
      let bodyMessage = {
        chat_user: payload.chatUser,
        message: {
          content: payload.message,
          image: body_image,
        },
      };
      let responseMessage = yield call(
        async () => await API.post(getURL("message", "ENTRYPOINT"), bodyMessage),
      );
      if (responseMessage.status === 200) { 
        responseMessage.data.data.forEach((message) => {
          messages.push({
            sender: message.sender,
            receiver: message.receiver,
            message: message.message,
            image: message?.path_image ? getFullURL('image/' + message.path_image, "ENTRYPOINT") : null,
            options: message?.options?.length 
              ? message.options.map((option) => getFullURL('image/' + option, "ENTRYPOINT")) 
              : null,
            is_option_action: true,
          });
        })
        yield put({
          type: "message/saveState",
          payload: {
            messages: messages,
            isLoading: false,
            currentMessage: "",
            currentImage: null,
          },
        });
      }
    } else {
      yield put({
        type: "message/saveState",
        payload: {
          isLoading: false,
          isShowImageUploadArea: true,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: false,
      },
    });
  }
}

export default function* watchAll() {
  yield all([
    yield takeEvery("message/getMessages", getMessages),
    yield takeEvery("message/sendMessage", sendMessage),
  ]);
}
