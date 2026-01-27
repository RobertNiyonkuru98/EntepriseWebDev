import time
import os
from main import xmlParsing
from DSAsearch import linear_search
from dictionarySearch import transaction_dictionary, dict_lookup

def run_performance_test():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xml_file = os.path.join(script_dir, 'modified_sms_v2.xml')
    transactions = xmlParsing(xml_file)
    transactions_dict = transaction_dictionary(transactions)

    target_ids = [t['id'] for t in transactions[:20]]

    start = time.perf_counter()
    for tid in target_ids:
        linear_search(transactions, tid)
    linear_time = time.perf_counter() - start

    start = time.perf_counter()
    for tid in target_ids:
        dict_lookup(transactions_dict, tid)
    dict_time = time.perf_counter() - start

    print(f"Results for 20 Records:")
    print(f"Linear Search Time: {linear_time:.8f}s")
    print(f"Dictionary Lookup Time: {dict_time:.8f}s")
    print(f"Efficiency Gain: {linear_time / dict_time:.2f}x faster")

if __name__ == "__main__":
    run_performance_test()