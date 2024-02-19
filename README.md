# TDB
Python wrapper for Transient Database (TDB) which is part of IraCluster.

### Requirements
This library depends on PyIraCluster, which is to be installed separately.

### Why does this library exist over PyIraCluster?
- Provides autocompletion with type annotations in the editor where python intellisense is available.
- The functions are written in snake case instead of pascal case (PEP 8)
- Reduces the parameters to be given as input for TDB functions which reduces the typo errors.
- Easy to get started as most of the configuration is optional by default.

### Install

```bash
apt install git # For Debian
pip install wheel
```
```
pip install git+https://github.com/epicira/pytdb.git
```

### Usage

```py
import PyIraCluster # the C++ python library import
from pytdb.tdb import TDB # the Python wrapper for TDB functions in PyIraCluster


def on_message(msg: any):
    print(msg)


def main():
    app_name = "sample-app"
    cluster_id = "my-cluster"

    # The below function is used to initialise IraCluster 
    # PyIraCluster.Cluster(your_application_name: str, cluster_id: str, callback: Callable)
    PyIraCluster.Cluster(app_name, cluster_id, on_message)
    tdb = TDB(cluster_id=cluster_id)
    sample_db = tdb.open(
        database_name="sample_db",
        init_query="""
        CREATE TABLE IF NOT EXISTS my_table_1 (
            a INT,
            b VARCHAR(30)
        );
        CREATE TABLE IF NOT EXISTS my_table_2 (
            m TEXT,
            n TEXT
        );
        """,
        index_query="""
        CREATE INDEX IF NOT EXISTS i1 ON my_table_1 (a);
        CREATE INDEX IF NOT EXISTS i2 ON my_table_2 (m);
        """
    )

    status = sample_db.execute('INSERT INTO my_table_1 (a, b) VALUES (1, "hello");')
    if status == "OK":
        print("success")
    _ = sample_db.execute('INSERT INTO my_table_2 (m, n) VALUES ("hello", "world");')
    
    my_table_1_count: int = sample_db.count("my_table_1")
    my_table_2_count: int = sample_db.count("my_table_2", where_clause='m="hello" AND n="world"')
```

### API

#### Constructor
```py
TDB(
    cluster_id: str,
    privacy_level: PyIraCluster.privacy = PyIraCluster.privacy.none,
    public_key: str = "",
    private_key: str = "",
    publish_changes: bool = True
)
```
The constructor will set all the provided configuration through arguments which will be used later while opening the database.

`cluster_id`: It is the only required argument which tells in which cluster the TDB is to be initialised. You need to give the same `cluster_id` that you passed to `PyIraCluster.Cluster` function.

`privacy_level`: This option allows you to have access control to the TDB. There are 4 privacy levels. `none`, `local`, `shared`, `private`.

##### Privacy Levels
- `private` option requires you to have both public and private keys to access the TDB.

- `shared` allows read only mode if you only have public key but allows writing if you have both keys.

- `none` has no access control. Anyone who is in the cluster can read and write to TDB.

- `local` does not have access control either. In `local` there is no replication of the TDB in different applications or within the processes of the same application. So, every instance of the application will have its own isolated TDB. 


`public_key`: RSA public key in plain or base64 encoded format.

`private_key`: RSA private key in plain or base64 encoded format.

`publish_changes`: If this option is true, the changes you make to the database are replicated to other copies of the database.

#### Open
```py
tdb.open(
    database_name: str,
    init_query: str = "",
    index_query: str = ""
)
```

`database_name`: name of the database

`init_query`: you can provide your database schema with multiple CREATE TABLE statements here.

`index_query`: just like init_query, this is used for CREATE INDEX statements.

#### Select
```py
tdb.select(
    query: str
)
```

#### Execute
```py
tdb.execute(
    query: str
    publish_changes: bool | None = None
)
```
`publish_changes` in execute function will override the setting that was provided in the TDB constructor. By default, it is set to None, that is, it will use the setting provided in the TDB constructor.

#### Execute async
```py
tdb.execute_async(
    query: str,
    publish_changes: bool | None = None
    execute_after: int = 0
)
```
`execute_after` accepts milliseconds after which the query should to be executed. Useful if you want to schedule query for later time and return immediately.

#### Count
```py
tdb.count(
    table_name: str,
    where_clause: str = ""
)
```
Used to count the number of records in the table just like `SELECT COUNT(*) FROM table_name`. This function is optimised for counting records and can be used instead of `tdb.execute` function if you want to count the records.

#### Destroy Local
```py
tdb.destroy_local()
```
This function will close the local TDB