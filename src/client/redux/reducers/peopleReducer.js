import { ActionTypes } from "../constants/actionTypes"

const initialState = {
    byUrl: {},
    linkedin: [],
    facebook: [],
    twitter: [],
    status: null,
}

export const peopleReducer = (state = initialState, {type, results}) => {
    // Errors?
    if (results && results.status !== 0) {
        return {...state, status: results.error};
    }

    switch(type) {
        case ActionTypes.FIND_PEOPLE:
            return {...initialState, status: 'running'};

        case ActionTypes.FIND_PEOPLE_STATUS:
            return {...state, status: results.result};

        case ActionTypes.FIND_PEOPLE_CANCEL:
            return {...state, status: (results.result)? null : 'running'};

        case ActionTypes.FIND_PEOPLE_RESULTS:
            let nextState = {...state, byUrl: {...state.byUrl}};

            for(let result of results.result) {
                nextState.byUrl[result.href] = result.text;

                if (/linkedin/.test(result.href)) {
                    nextState.linkedin = [...nextState.linkedin, result.href];
                } else if (/twitter/.test(result.href)) {
                    nextState.twitter = [...nextState.twitter, result.href];
                } if (/facebook/.test(result.href)) {
                    nextState.facebook = [...nextState.facebook, result.href];
                }
            }

            return nextState;
    }

    return state;
}
