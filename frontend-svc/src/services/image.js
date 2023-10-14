import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put, select } from "redux-saga/effects";
import { getURL } from "utils/url";
import notification from "components/Notification";
import i18n from "i18n";


function* addNewUpload({ payload }) {
  try {
    let formData = new FormData();
    payload.images.forEach((label) => {
        label.urls.forEach((imageUrl) => {
            formData.append("files", imageUrl.file);
        })
    })
    let response = yield call(
      async () =>
        await API.post(getURL("image", "META"), formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }),
    );
    if (response.status === 200) {
      notification("success", i18n.t("notify.successAddNewUpload"));
    }
  } catch (error) {
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

function* getUploadedImages({ payload }) {
  try {
    let response = yield call(
      async () => await API.get(getURL("image", "META")),
    );
    if (response.status === 200) {
      yield put({
        type: "image/saveState",
        payload: {
          uploadedImages: response.data.data,
          isLoading: false,
        },
      });
      notification("success", i18n.t("notify.successGetUploadedImages"));
    }
  } catch (error) {
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

function* getImages({ payload }) {
  const state = yield select();
  try {
    yield put({
      type: "message/saveState",
      payload: {
        isLoading: true,
      },
    });
    let body_image = null;
    if (payload.image) {
      body_image = {
        data: payload?.image.dataURL,
        filename: payload?.image.file.name,
      };
    }
    let body = {
      chat_id: payload.chatId,
      message: {
        message: payload.message,
        receiver: payload.receiver,
        image: body_image,
      },
    };
    let response = yield call(
      async () => await API.post(getURL("message", "ENTRYPOINT"), body),
    );
    if (response.status === 200) {
      let messages = [...state.message.messages];
      // if (response.data?.data?.length > 0) {
      //   response.data.data.forEach((messageObj) => {
      //     messages.push({
      //       fromSelf: messageObj.is_from_self,
      //       message: messageObj.message,
      //       image: messageObj.path_image
      //         ? process.env.REACT_APP_IMAGE_URL + messageObj.path_image
      //         : null,
      //     });
      //   });
      // }
      messages.push({
        sender: state.account.username,
        receiver: payload.receiver,
        message: payload.message,
        image: null,
      });
      yield put({
        type: "message/saveState",
        payload: {
          messages: messages,
          isLoading: false,
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
    yield takeEvery("image/getImages", getImages),
    yield takeEvery("image/addNewUpload", addNewUpload),
    yield takeEvery("image/getUploadedImages", getUploadedImages),
  ]);
}
