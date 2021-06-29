import axios from 'axios';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Card } from 'semantic-ui-react';

import { findPeopleResults } from '../redux/actions/peopleActions';

const PeopleResults = () => {
    const dispatch = useDispatch();
    const people = useSelector((state) => state.people);
    const status = people.status;

    // Poll for results
    useEffect(() => {
        // Exit early if not running
        if (!status) return;

        const timer = setInterval(() => axios
            .get('/api/v1/scraper/google/findpeople/results')
            .then((response) => {
                dispatch(findPeopleResults(response.data));
            })
            .catch((err) => {
                console.log(err);
            })

        , 10000);

        return () => clearInterval(timer);
    });

    // Get items
    let items = [];
    
    for (let url in people.byUrl) {
        const meta = (/linkedin/.test(url))
            ? 'Linkedin'
            : (/twitter/.test(url))
                ? 'Twitter'
                : (/facebook/.test(url))
                    ? 'Facebook'
                    : 'Unknown';

        items.push({
            header: <a href={url}>{people.byUrl[url]}</a>,
            meta,
        });
    }

    return (
        <Card.Group items={items} />
    );
};

export default PeopleResults;
