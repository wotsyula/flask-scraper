import { createStore, applyMiddleware } from 'redux';
import { devToolsEnhancer } from 'redux-devtools-extension';

import reducers from "./reducers";

const store = createStore(reducers, {}, devToolsEnhancer(
    // options like actionSanitizer, stateSanitizer
));

export default store;
