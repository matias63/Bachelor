import current
import time


    



def timer(search_word):
    global test_samples_modifier
    try:
        start_time = time.time()
        current.thread_search(search_word)
        end_time = time.time() - start_time
        return end_time
    except:
        test_samples_modifier -=1
        return 0.0

def timer_without_indexing(search_word):
    global test_samples_modifier
    try:
        start_time = time.time()
        current.thread_search_before_indexing(search_word)
        end_time = time.time() - start_time
        return end_time
    except:
        test_samples_modifier -=1
        return 0.0

def timer_image_processing(search_word):
    global test_samples_modifier
    try:
        start_time = time.time()
        cache = current.thread_search(search_word)
        current.image_processing(cache,search_word)
        end_time = time.time() - start_time
        return end_time
    except:
        test_samples_modifier -=1
        return 0.0
    
def test_search(search_word,test_samples):
    total_time = 0.0
    test_samples_modifier = test_samples
    print(f"search {search_word}")
    print("With indexing")
    for i in range(test_samples):
        end_time = timer(search_word)
        total_time += end_time
    average_search_time = total_time/test_samples_modifier
    print("average search time when performing",test_samples_modifier, "searches of", search_word, "is:", average_search_time)

def test_search_without_indexing(search_word,test_samples):
    total_time = 0.0
    test_samples_modifier = test_samples
    print(f"search {search_word}")
    print("Without indexing")
    for i in range(test_samples):
        end_time = timer_without_indexing(search_word)
        total_time += end_time
    average_search_time = total_time/test_samples_modifier
    print("average search time when performing",test_samples_modifier, "searches of", search_word, "is:", average_search_time)



def main():
    print("BM Good suffix rule")
    test_search("elf",100)  
    test_search_without_indexing("elf",100)  
    test_search("red",100)
    test_search_without_indexing("red",100)
    test_search("goblin",100)
    test_search_without_indexing("goblin",100)

if __name__ == main():
    main()