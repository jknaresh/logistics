import json

from django.http import JsonResponse
from django.shortcuts import render

from django.views import View

from arango.connection import db_conn


class HomeView(View):
    permission_checker = None

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)

    def post(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)


class Initialize(View):
    permission_checker = None

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)

    def post(self, request, *args, **kwargs):
        return render(
            request, self.template_name, context=locals(),
            content_type="text/html", status=200)


class Provider(View):
    permission_checker = None

    provider_collection = db_conn['provider']

    res = dict()
    res["status"] = False

    def get(self, request, *args, **kwargs):
        # list for return data
        all_providers_list = list()

        # read data from request
        email = request.GET.get("email")

        # check, all records or only required one?
        if email:
            try:
                # fetch existing document
                ap = self.provider_collection.fetchDocument(key=email)

                # preparing data dict
                data = dict()

                # prepare required data and assignment
                data['name'] = ap["name"]
                data["email"] = ap["email"]
                data["ph_no"] = ap["mobile"]
                data["language"] = ap["language"]
                data["currency"] = ap["currency"]

                # preparing for return data
                all_providers_list.append(data)
            except Exception as e:
                pass

        else:

            # fetch all document from collection
            all_providers = self.provider_collection.fetchAll()

            # read one by one document
            for ap in all_providers:

                # preparing data dict
                data = dict()

                # prepare required data and assignment
                data['name'] = ap["name"]
                data["email"] = ap["email"]
                data["ph_no"] = ap["mobile"]
                data["language"] = ap["language"]
                data["currency"] = ap["currency"]

                # preparing for return data
                all_providers_list.append(data)

        # return json data
        return JsonResponse(all_providers_list, safe=False)

    def post(self, request, *args, **kwargs):
        """
        POST data parameters
        # name, email, mobile, language, currency

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # get data from POST object
        email = request.POST.get("email")
        action = request.POST.get("action")

        # Check, to delete document. post data has action == delete
        if action == "delete":
            try:
                # Get document using key
                pd = self.provider_collection.fetchDocument(key=email)

                # delete document
                pd.delete()

                # return status
                self.res["status"] = True
            except Exception as e:
                pass

        else:

            # get data from POST object
            name = request.POST.get("name")
            mobile = request.POST.get("mobile")
            language = request.POST.get("language")
            currency = request.POST.get("currency")
            try:

                # fetch existing document
                pd = self.provider_collection.fetchDocument(key=email)

                # check, update name if input != ""
                if name:
                    pd['name'] = name

                # check, update mobile if input != ""
                if mobile:
                    pd["ph_no"] = mobile

                # check, update language if input != ""
                if language:
                    pd["language"] = language

                # check, update currency if input != ""
                if currency:
                    pd["currency"] = currency

                # update data
                pd.save()

                # return status
                self.res["status"] = True

            except Exception as e:

                # data dict
                data = dict()
                data['name'] = name
                data["email"] = email
                data["ph_no"] = mobile
                data["language"] = language
                data["currency"] = currency

                # preparing document object
                provider_document = self.provider_collection.createDocument()

                # assigning data to Document
                provider_document.set(data)

                # to fetch by key, using email id for unique
                provider_document._key = email

                # save data
                provider_document.save()

                # return status
                self.res["status"] = True

        # return json data
        return JsonResponse(self.res, safe=False)


class ServiceArea(View):
    """
    provider email, geojson (polygon), polygon_name, price
    """
    permission_checker = None

    service_area_collection = db_conn['service_area']

    res = dict()
    res["status"] = False

    def get(self, request, *args, **kwargs):
        # list for return data
        all_providers_list = list()

        # read data from request
        email = request.GET.get("email")
        # check, all records or only required one?
        if email:
            try:
                # fetch existing document
                sa = self.service_area_collection.fetchDocument(key=email)

                # preparing data dict
                data = dict()

                # prepare required data and assignment
                j = sa["geojson"]
                data['geojson'] = j.store
                data["polygon_name"] = sa["polygon_name"]
                data["price"] = sa["price"]

                # preparing for return data
                all_providers_list.append(data)
            except Exception as e:
                pass
        else:
            # fetch all document from collection
            all_sa = self.service_area_collection.fetchAll()

            # read one by one document
            for sa in all_sa:
                # preparing data dict
                data = dict()

                # prepare required data and assignment
                j = sa["geojson"]
                data['geojson'] = j.store
                data["email"] = sa._key
                data["polygon_name"] = sa["polygon_name"]
                data["price"] = sa["price"]

                # preparing for return data
                all_providers_list.append(data)

        # return json data
        return JsonResponse(all_providers_list, safe=False)

    def post(self, request, *args, **kwargs):

        # get data from POST object
        email = request.POST.get("email")
        action = request.POST.get("action")

        # Check, to delete document. post data has action == delete
        if action == "delete":
            try:
                # Get document using key
                sa = self.service_area_collection.fetchDocument(key=email)

                # delete document
                sa.delete()

                # return status
                self.res["status"] = True
            except Exception as e:
                pass

        else:

            # get data from POST object

            geojson = request.POST.get("geojson")
            polygon_name = request.POST.get("polygon_name")
            price = request.POST.get("price")
            try:
                # fetch existing document
                sa = self.service_area_collection.fetchDocument(key=email)

                # check, update geojson if input != ""
                if geojson:
                    sa['geojson'] = geojson

                # check, update polygon_name if input != ""
                if polygon_name:
                    sa["polygon_name"] = polygon_name

                # check, update price if input != ""
                if price:
                    sa["price"] = price

                # update data
                sa.save()

                # return status
                self.res["status"] = True

            except Exception as e:

                # data dict
                sa = dict()
                sa['geojson'] = json.loads(geojson)
                sa["polygon_name"] = polygon_name
                sa["price"] = price

                # preparing document object
                service_document = self.service_area_collection.createDocument()

                # assigning data to Document
                service_document.set(sa)

                # to fetch by key, using email id for unique
                service_document._key = email

                # save data
                service_document.save()

                # return status
                self.res["status"] = True

        # return json data
        return JsonResponse(self.res, safe=False)


class ServiceProvider(View):
    permission_checker = None

    def get(self, request, *args, **kwargs):
        """
        http://127.0.0.1:8000/service-provider/?lat=78.4529560804367&lng=17.4173210167708

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # list for return data
        all_service_providers_list = list()

        # read data from request
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")

        # By request, every data is string, as vertices are float values. we are converting to float.
        t1 = [float(lat), float(lng)]

        # preparing target dict for input data
        target = dict()
        target["type"] = "Polygon"

        # least 4 vertices, required to check target is in side polygon or not?
        target["coordinates"] = [[t1, t1, t1, t1]]

        # Preparing AQL Query, @target is place holder. Inner for is for join with provider data to fetch name of
        # provider
        aql = """
            FOR doc IN service_area
                FILTER GEO_CONTAINS(doc.geojson, @target)
                FOR d1 IN provider
                    FILTER doc._key == d1._key
                RETURN {"name": d1.name, "polygon_name": doc.polygon_name, "price": doc.price, "geojson": doc.geojson}
        """

        # prepare bind data dict
        bind = dict()
        bind["target"] = target

        # execute AQL using AQLQuery method
        query_result = db_conn.AQLQuery(aql, rawResults=True, bindVars=bind)

        # read query result and make proper json serializable
        for row in query_result:
            all_service_providers_list.append(row)

        # return json data
        return JsonResponse(all_service_providers_list, safe=False)
