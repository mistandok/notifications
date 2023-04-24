db = db.getSiblingDB('ugc');

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
                required: ["user_id"],
                properties: {
                    rating: {
                        bsonType: "int",
                        description: "can only be a integer",
                        minimum: 1,
                        maximum: 10
                    }
                }
            }
        }
    },
);