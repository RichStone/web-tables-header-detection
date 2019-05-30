import { MongoClient } from 'mongodb';
import config from 'config';

export const connectToDB = () =>
    MongoClient
        .connect(config.get('mongodb.url'), { useNewUrlParser: true })
        .then(client => {
            const db = client.db(config.get('mongodb.db'));
            return {
                client,
                db,
                tables: db.collection(config.get('mongodb.collections.tables'))
            };
        });