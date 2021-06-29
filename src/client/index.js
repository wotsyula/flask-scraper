/**
 * @date            27/06/2021
 * @author          Walter Otsyula <wotsyula@gmail.com>
 * @description
 * Main entry point for webpack bundle.
 */

import 'semantic-ui-css/semantic.min.css'
import 'regenerator-runtime/runtime';

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';

import App from './containers/App.js';
import store from './redux/store.js';

ReactDOM.render(
    <React.StrictMode>
        <Provider store={store}>
            <App />
        </Provider>
    </React.StrictMode>,
    document.getElementById('root'),
);
