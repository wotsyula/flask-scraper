/**
 * @date            28/06/2021
 * @author          Walter Otsyula <wotsyula@gmail.com>
 * @description
 * Main entry point for webpack bundle.
 */

import "regenerator-runtime/runtime";
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './App.js';

import store from './redux/store.js';

ReactDOM.render(
    <React.StrictMode>
        <Provider store={store}>
            <App />
        </Provider>
    </React.StrictMode>,
    document.getElementById('root'),
);
