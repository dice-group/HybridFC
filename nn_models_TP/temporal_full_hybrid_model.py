from .base_model import *

import torch.nn as nn
from numpy.random import RandomState
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import random
import numpy as np
# from pytorchtools import EarlyStopping
import torch
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)



class TemporalFullHybridModel(BaseKGE):

    def __init__(self, args):
        super().__init__(args)
        self.name = 'TemporalModel'
        self.ent_embeddings = args.dataset.emb_entities
        self.rel_embeddings = args.dataset.emb_relation
        self.tim_embeddings = args.dataset.emb_time

        self.embedding_dim = args.embedding_dim
        self.num_entities = args.num_entities
        self.num_relations = args.num_relations
        self.num_times = args.num_times
        self.loss = torch.nn.BCELoss()
        self.sentence_dim = int(args.sentence_dim) * 3

        for i, word in enumerate(self.ent_embeddings):
            self.embedding_dim = len(word)
            break
        for i, word in enumerate(self.rel_embeddings):
            self.embedding_dim_rel = len(word)
            break
        for i, word in enumerate(self.tim_embeddings):
            self.embedding_dim_tim = len(word)
            break

        self.shallom_width = int(25.6 * self.embedding_dim)
        self.shallom_width2 = int(12.8 * self.embedding_dim)
        self.shallom_width3 = int(1 * self.embedding_dim)
        self.sen_embeddings_train = args.dataset.emb_sentences_train
        self.sen_embeddings_test = args.dataset.emb_sentences_test
        self.sen_embeddings_valid = args.dataset.emb_sentences_valid

        self.entity_embeddings = nn.Embedding(self.num_entities, self.embedding_dim)
        self.relation_embeddings = nn.Embedding(self.num_relations, self.embedding_dim_rel)
        self.time_embeddings = nn.Embedding(self.num_times, self.embedding_dim_tim)

        self.sentence_embeddings_train = nn.Embedding(len(self.sen_embeddings_train), self.sentence_dim)
        self.sentence_embeddings_test = nn.Embedding(len(self.sen_embeddings_test), self.sentence_dim)
        self.sentence_embeddings_valid = nn.Embedding(len(self.sen_embeddings_valid), self.sentence_dim)

        self.entity_embeddings.load_state_dict(
            {'weight': torch.tensor(self.convrt_embeddings(args.num_entities, self.embedding_dim, self.ent_embeddings))})

        self.relation_embeddings.load_state_dict(
            {'weight': torch.tensor(self.convrt_embeddings(args.num_relations, self.embedding_dim_rel, self.rel_embeddings))})

        self.sentence_embeddings_train.load_state_dict(
            {'weight': torch.tensor(self.convrt_embeddings(len(self.sen_embeddings_train), self.sentence_dim, self.sen_embeddings_train))})

        self.sentence_embeddings_test.load_state_dict(
            {'weight': torch.tensor(
                self.convrt_embeddings(len(self.sen_embeddings_test), self.sentence_dim, self.sen_embeddings_test))})
        self.sentence_embeddings_valid.load_state_dict(
            {'weight': torch.tensor(
                self.convrt_embeddings(len(self.sen_embeddings_valid), self.sentence_dim, self.sen_embeddings_valid))})
        self.entity_embeddings.weight.requires_grad = False
        self.relation_embeddings.weight.requires_grad = False
        self.sentence_embeddings_test.weight.requires_grad = False
        self.sentence_embeddings_valid.weight.requires_grad = False
        self.sentence_embeddings_train.weight.requires_grad = False

        self.kg_classification_layer = nn.Sequential(torch.nn.Linear(self.embedding_dim * 2 + self.embedding_dim_rel +self.embedding_dim_tim, self.shallom_width),
                                                     nn.BatchNorm1d(self.shallom_width),
                                                     nn.ReLU(),
                                                     nn.Dropout(0.50),
                                                     torch.nn.Linear(self.shallom_width, self.shallom_width))

        self.sentence_classification_layer = nn.Sequential(torch.nn.Linear(self.sentence_dim, self.shallom_width),
                                                           nn.BatchNorm1d(self.shallom_width),
                                                           nn.ReLU(),
                                                           nn.Dropout(0.50),
                                                           torch.nn.Linear(self.shallom_width, self.shallom_width))

        self.final_classification_layer = nn.Sequential(torch.nn.Linear(self.shallom_width * 2, self.shallom_width),
                                                        nn.BatchNorm1d(self.shallom_width),
                                                        nn.ReLU(),
                                                        nn.Dropout(0.50),
                                                        torch.nn.Linear(self.shallom_width, 1))

    def forward_triples(self, e1_idx, rel_idx, e2_idx, tim_idx, sen_idx, type="training"):
        # print(sen_idx)
        emb_head_real = self.entity_embeddings(e1_idx)
        emb_rel_real = self.relation_embeddings(rel_idx)
        emb_tail_real = self.entity_embeddings(e2_idx)
        emb_tim_real = self.time_embeddings(tim_idx)
        x = torch.cat([emb_head_real, emb_rel_real, emb_tail_real, emb_tim_real], 1)
        triplet_embedding = self.kg_classification_layer(x)
        emb_sen = []
        if type.__contains__("training"):
            emb_sen = self.sentence_embeddings_train(sen_idx)
        elif type.__contains__("valid"):
            emb_sen = self.sentence_embeddings_valid(sen_idx)
        else:
            emb_sen = self.sentence_embeddings_test(sen_idx)
        sentence_embedding = self.sentence_classification_layer(emb_sen)
        z = torch.cat([triplet_embedding, sentence_embedding], 1)
        return torch.sigmoid(self.final_classification_layer(z))


