class QueryUtils:

    @staticmethod
    def remove_extra_spaces(sentence: str) -> str:
        return ' '.join(sentence.split())

    @staticmethod
    def not_valid_query(query):
        forbidden = ['MATCH () RETURN *']
        return any(f in query for f in forbidden)

    @staticmethod
    def split_by_space_no_quotes(sentence) -> list[str]:
        return list(filter(lambda x: x != '', sentence.split(' ')))

    @staticmethod
    def remove_quotes_if_needed(token):
        if isinstance(token, str) and token.startswith('\'') and token.endswith('\''):
            return token[1:-1]
        return token

    @staticmethod
    def _unfold_graph_resp(resp):
        return [v for item in resp.data() for _, v in item.items()]

    @staticmethod
    def _escape_special_chars(values):
        for i, v in enumerate(values):
            if isinstance(v, str):
                values[i] = v.replace("'", "\\'")

    @staticmethod
    def equal_simple_query_results(result1, result2):
        if len(result1) != len(result2):
            return False
        
        elif result1 == result2:
            return True

        values1 = [data[list(data.keys())[0]] for data in result1]
        values2 = [data[list(data.keys())[0]] for data in result2]
        return values1 == values2
    
    @staticmethod
    def equal_classic_query_results(result1, result2):
        try:
            values1 = {data[list(data.keys())[0]] for data in result1}
            values2 = {data for data in result2.split('|')}
        except:
            return False
        return values1 == values2