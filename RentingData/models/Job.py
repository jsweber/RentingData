from elasticsearch_dsl import DocType, Date, Boolean, analyzer, Completion, Keyword, Text, Integer, Nested
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Job(DocType):
    job_id = Keyword()
    url = Keyword()
    job_name = Text(analyzer='ik_max_word')
    location = Text(analyzer='ik_max_word')
    city = Keyword()
    orginal_salary = Keyword()
    low_salary = Integer()
    high_salary = Integer()
    middle_salary = Integer()
    publish_time = Date()
    crawl_time = Date()
    welfare = Text(analyzer='ik_max_word') #逗号合并字符串
    describe = Text(analyzer='ik_max_word')
    company = Text(analyzer='ik_max_word')
    requires = Nested(
        properties = {
            'degree': Keyword(),
            'orginal_degree': Text(analyzer='ik_max_word'),
            'exp': Integer(),
            'orginal_exp': Text(analyzer='ik_max_word'),
            'language': Text(analyzer='ik_max_word'),
            'age': Integer(),
            'orginal_age': Text(analyzer='ik_max_word'),
        }
    )

    class Meta:
        index = 'job_data_v2'
        doc_type = 'job'

if __name__ == '__main__':
    Job.init()

