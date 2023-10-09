import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put } from "redux-saga/effects";
import { getURL } from "utils/url";
import notification from "components/Notification";

function* getAllChats({ payload }) {
  try {
    yield put({
      type: "chat/saveState",
      payload: {
        isLoading: true,
      },
    });
    let response = yield call(
      async () =>
        await API.get(getURL("chat", "BACKEND"), {
          params: {
            username: payload.username,
          },
        }),
    );
    if (response.status === 200) {
      yield put({
        type: "chat/saveState",
        payload: {
          chats: response.data.data.map(chat => ({
            _id: chat.id,
            name: chat.name,
            avatarImage: null,
          })),
          isLoading: false,
        },
      });
    }
  } catch (error) {
    yield put({
      type: "chat/saveState",
      payload: {
        isLoading: false,
      },
    });
    notification(
      "error",
      error.response.data?.message ? error.response.data.message : error.message,
    );
  }
}

// function* createNewChat({ payload }) {
//   try {
//     yield put({
//       type: "user/saveState",
//       payload: {
//         isLoading: true,
//       },
//     });
//     console.log("aaaa", getURL("/user/login", "BACKEND"));
//     let response = yield call(
//       async () =>
//         await API.post("user/login", {
//           username: payload.username,
//           password: payload.password,
//         }),
//     );
//     console.log("SSSSSSSSSSS");
//     console.log("response", response);
//     if (response.status === 200) {
//       localStorage.setItem("username", payload.username);
//       yield put({
//         type: "user/saveState",
//         payload: {
//           isLoading: false,
//         },
//       });
//       //   notification("success", response.data.message);
//       window.location.href = "/";
//     }
//   } catch (error) {
//     yield put({
//       type: "user/saveState",
//       payload: {
//         isLoading: false,
//       },
//     });
//     notification(
//       "error",
//       error.response.data?.message ? error.response.data.message : error.message,
//     );
//   }
// }

export default function* watchAll() {
  yield all([
    yield takeEvery("chat/getAllChats", getAllChats),
    // yield takeEvery("chat/createNewChat", createNewChat),
  ]);
}