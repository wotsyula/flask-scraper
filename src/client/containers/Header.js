import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { findPeople, findPeopleStatus } from '../redux/actions/peopleActions';

const Header = () => {
    let [query, setQuery] = useState('');
    const dispatch = useDispatch();
    const people = useSelector((state) => state.people);

    // Poll status
    useEffect(() => {
        const timer = setInterval(() => axios
            .get('http://localhost:5000/api/v1/scraper/google/findpeople/status')
            .then((response) => {
                dispatch(findPeopleStatus(response.data));
            })
            .catch((err) => {
                console.log(err);
            })

        , 30000);

        return () => clearInterval(timer);
    });

    const doFindPeople = async () => {

        const response = await axios
            .get('http://localhost:5000/api/v1/scraper/google/findpeople', {params: {query}})
            .catch((err) => {
                console.log(err);

                return {
                    status: 911,
                    error: 'Unknown error',
                    results: null,
                }
            });

        dispatch(findPeople(response.data));
    };

    const onChange = (event) => {
        setQuery(event.target.value);
    };

    // Generate status text
    let status = '';

    if (typeof people.status === 'string') {
        status = people.status.toUpperCase();
    }

    if (people.linkedin.length > 1) {
        status += ' | L (' + people.linkedin.length + ')';
    }

    if (people.twitter.length > 1) {
        status += ' | T (' + people.twitter.length + ')';
    }

    if (people.facebook.length > 1) {
        status += ' | F (' + people.facebook.length + ')';
    }

    return (
        <div className="ui fixed menu">
            <div className="ui container center">
                <h2>Demo</h2> &nbsp;
                <input id="query" type="text" value={query} onChange={onChange} /> &nbsp;
                <button onClick={doFindPeople}>Search</button>  &nbsp; &nbsp; &nbsp;
                <span>{status}</span>

            </div>
        </div>
    );
};

export default Header;
