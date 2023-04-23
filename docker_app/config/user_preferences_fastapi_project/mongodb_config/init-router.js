sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

sh.enableSharding("preferences");

db = db.getSiblingDB('preferences');

db.createCollection(
    "user_preferences",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id"]
            }
        }
    },
);

sh.shardCollection("preferences.user_preferences", {"user_id": 1}, true);