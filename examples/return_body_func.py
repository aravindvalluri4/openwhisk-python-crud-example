def main(args):
    try:
        decoded = args['__ow_body']
        print(args)
        return {"body": decoded}
    except Exception as e:
        print(args)
        print(e)
        return {"body": "Could not decode body from Base64."}
