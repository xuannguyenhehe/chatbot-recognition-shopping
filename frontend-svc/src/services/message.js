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
              ? messageObj.options.map((option) => option.includes('/') ? getFullURL('image/' + option, "ENTRYPOINT") : option) 
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
    let currentOptions = null;
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
      if (payload?.isBackup !== null) {
        bodyMessage.is_backup = payload.isBackup
      }
      if (payload?.offsetImage !== null) {
        bodyMessage.offset_image = payload.offsetImage
      }
      let responseMessage = yield call(
        async () => await API.post(getURL("message", "ENTRYPOINT"), bodyMessage),
      );
      if (responseMessage.status === 200) { 
        responseMessage.data.data.forEach((message) => {
          currentOptions = message?.options?.length 
            ? message.options.map((option) => option.includes('/') ? getFullURL('image/' + option, "ENTRYPOINT") : option) 
            : null;
          messages.push({
            sender: message.sender,
            receiver: message.receiver,
            message: message.message,
            image: message?.path_image ? getFullURL('image/' + message.path_image, "ENTRYPOINT") : null,
            options: currentOptions,
            is_option_action: true,
          });
        })
        yield put({
          type: "message/saveState",
          payload: {
            messages: messages,
            isLoading: false,
            currentMessage: "",
            backupMessage: payload.message,
            currentImage: null,
            backupImage: payload?.image,
            currentOptions: currentOptions,
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

function* sendChoseImageMessage({ payload }) {
  const state = yield select();
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: true,
      },
    });
    let messages = [...state.message.messages];
    let bodyMessage = {
      chat_user: payload.chatUser,
      path_image: payload.pathImage,
    };
    let responseMessage = yield call(
      async () => await API.post(getURL("message/choose_image", "ENTRYPOINT"), bodyMessage),
    );
    if (responseMessage.status === 200) { 
      responseMessage.data.data.forEach((message) => {
        messages.push({
          sender: message.sender,
          receiver: message.receiver,
          message: message.message,
          image: message?.path_image ? getFullURL('image/' + message.path_image, "ENTRYPOINT") : null,
          options: message?.options,
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
  } catch (error) {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: false,
      },
    });
  }
}

function* sendSpecifiedMessage({ payload }) {
  const state = yield select();
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: true,
      },
    });
    let messages = [...state.message.messages];
    let bodyMessage = {
      chat_user: payload.chatUser,
      message: payload.message,
    };
    let responseMessage = yield call(
      async () => await API.post(getURL("message/specified", "ENTRYPOINT"), bodyMessage),
    );
    if (responseMessage.status === 200) { 
      responseMessage.data.data.forEach((message) => {
        messages.push({
          sender: message.sender,
          receiver: message.receiver,
          message: message.message,
          image: null,
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
    yield takeEvery("message/sendChoseImageMessage", sendChoseImageMessage),
    yield takeEvery("message/sendSpecifiedMessage", sendSpecifiedMessage),
  ]);
}
