import API from "plugins/http-proxy/http-client";
import { all, takeEvery, call, put } from "redux-saga/effects";
import { getURL } from "utils/url";
import notification from "components/Notification";
import i18n from "i18n";


function* getAdditionalIntents({ payload }) {
    try {
        yield put({
            type: "qa/saveState",
            payload: {
                isLoading: true,
            },
        });
        let response = yield call(
            async () =>
                await API.get(getURL("qa", "ENTRYPOINT"))
        );
        if (response.status === 200) {
            yield put({
                type: "qa/saveState",
                payload: {
                    intents: response.data?.data?.map(intent => ({
                        questions: intent.questions.join(';\n'),
                        answer: intent.answer,
                        keyword: intent.keyword,
                        isModified: false,
                    })),
                    isLoading: false,
                },
            });
            notification("success", i18n.t("notify.successGetQA"));
        }
    } catch (error) {
        yield put({
            type: "qa/saveState",
            payload: {
                isLoading: false,
            },
        });
        notification(
            "error",
            error.response?.data?.message ? error.response?.data.message : error.message,
        );
    }
}

function* createNewIntents({ payload }) {
    try {
        let response = yield call(
            async () =>
                await API.post(getURL("qa", "ENTRYPOINT"), {
                    intents: payload.intents.map(intent => ({
                        questions: intent.questions.split(';\n'),
                        answer: intent.answer,
                        keyword: intent.keyword,
                    })),
                })
        );
        if (response.status === 200) {
            yield put({
                type: "qa/getAdditionalIntents",
            });
        }
    } catch (error) {
        notification(
            "error",
            error.response.data?.message ? error.response.data.message : error.message,
        );
    }
}

function* trainIntents({ payload }) {
    try {
        let response = yield call(
            async () =>
                await API.post(getURL("rasa", "ENTRYPOINT"))
        );
        yield put({
            type: "qa/saveState",
            payload: {
                statusTrain: 'training',
            },
        });
        if (response.status === 200) {
            yield put({
                type: "qa/getAdditionalIntents",
            });
        }
    } catch (error) {
        notification(
            "error",
            error.response?.data?.message ? error.response?.data.message : error.message,
        );
    }
}

function* checkStatusTrain({ payload }) {
    try {
        let response = yield call(
            async () =>
                await API.get(getURL("rasa/status-train", "ENTRYPOINT"))
        );
        if (response.status === 200) {
            yield put({
                type: "qa/saveState",
                payload: {
                    statusTrain: response.data?.data,
                },
            });
        }
    } catch (error) {
        notification(
            "error",
            error.response.data?.message ? error.response.data.message : error.message,
        );
    }
}

function* approveNewCheckpoint({ payload }) {
    try {
        let response = yield call(
            async () =>
                await API.post(getURL("rasa/approve", "ENTRYPOINT"))
        );
        if (response.status === 200) {
            yield put({
                type: "qa/saveState",
                payload: {
                    statusTrain: "approved",
                },
            });
        }
    } catch (error) {
        notification(
            "error",
            error.response.data?.message ? error.response.data.message : error.message,
        );
    }
}

export default function* watchAll() {
    yield all([
        yield takeEvery("qa/getAdditionalIntents", getAdditionalIntents),
        yield takeEvery("qa/createNewIntents", createNewIntents),
        yield takeEvery("qa/trainIntents", trainIntents),
        yield takeEvery("qa/checkStatusTrain", checkStatusTrain),
        yield takeEvery("qa/approveNewCheckpoint", approveNewCheckpoint),
    ]);
}
