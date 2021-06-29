import { combineReducers } from "redux";
import { peopleReducer } from "./peopleReducer";

const reducers = combineReducers({
    people: peopleReducer,
});

export default reducers;
