/**
 * @date            28/036/2021
 * @author          Walter Otsyula <wotsyula@gmail.com>
 * @description
 * Defines the main react component.
 */

/** @module flask-scraper/App */

import React from 'react';
import {hot} from "react-hot-loader";
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import './App.css';
import Header from './containers/Header';
import PeopleResults from './containers/PeopleResults';

function App() {

    return(
        <div className="App">
            <Router>
                <Header />
                <Switch>
                    <Route component={PeopleResults} />
                </Switch>
            </Router>
        </div>
    );
}

export default hot(module)(App);
