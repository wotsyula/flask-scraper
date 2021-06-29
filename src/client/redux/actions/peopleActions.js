import { ActionTypes } from "../constants/actionTypes";

export const findPeople = (results) => {
    return {
        type: ActionTypes.FIND_PEOPLE,
        results: results,
    };
};

export const findPeopleCancel = (results) => {
    return {
        type: ActionTypes.FIND_PEOPLE_CANCEL,
        results: results,
    }
}

export const findPeopleStatus = (results) => {
    return {
        type: ActionTypes.FIND_PEOPLE_STATUS,
        results: results,
    }
}

export const findPeopleResults = (results) => {
    return {
        type: ActionTypes.FIND_PEOPLE_RESULTS,
        results: results,
    }
}
