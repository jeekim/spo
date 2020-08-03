import nox


@nox.session
def tests(session):
    session.install("-r", "requirements.txt")
    session.install('pytest')
    session.run(
        'pytest', '-v',
        env={
            # "DATA_DIR": "$(pwd)/data/tests",
            # "CORENLP_HOME": "$(pwd)/model/stanford-corenlp-4.0.0"
            # "CORENLP_HOME": "$(pwd)/model/stanford-corenlp-4.0.0"
        }
    )

